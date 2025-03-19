import streamlit as st
import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai
from dotenv import load_dotenv
import os

# -------------------- Load Environment Variables --------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# -------------------- Streamlit UI Configuration --------------------
st.set_page_config(page_title="📄 PDF Summarizer", layout="wide")

# -------------------- Custom Styling --------------------
st.markdown("""
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');

        .main {
            background: linear-gradient(to right, #f0f0f0, #d9e4f5);
            color: #333;
        }
        
        .main-title {
            text-align: center;
            font-size: 70px;
            font-family: 'Poppins', sans-serif;
            font-weight: bold;
            color: white;
            background: linear-gradient(90deg, #4CAF50, #2196F3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 3px 3px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease-in-out;
        }

        .main-title:hover {
            transform: scale(1.15);
        }

        /* Sidebar Styling */
        .sidebar-heading {
            font-size: 22px;
            color: #ffffff;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 15px;
        }
        .sidebar-heading.upload {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
        }
        .sidebar-heading.language {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
        }

        /* Sidebar Box Styling with Hover Effect */
        .stFileUploader, .stSelectbox {
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .stFileUploader:hover, .stSelectbox:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        }

        /* Box Shadow and Hover Effect for Text Areas */
        .stTextArea, .st-expander {
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            transition: all 0.3s;
        }
        .stTextArea:hover, .st-expander:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        }

        /* Hover & Box Shadow for Extracted Text & Summary */
        .custom-box {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            padding: 15px;
            border-radius: 12px;
           
            background:#f9f9f9 /*#ffffff;  White background for readability */
            color: #333; 
        }
        .custom-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }
        
        
        /* Buttons with Hover Effects */
        .stButton>button {
            background: linear-gradient(135deg, #4CAF50, #2196F3);
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px 24px;
            transition: all 0.3s;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        .stButton>button:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }

        /* Download Button */
        .stDownloadButton>button {
            background: linear-gradient(135deg, #4CAF50, #2196F3);
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px 24px;
            transition: all 0.3s;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        .stDownloadButton>button:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }

         /* Sidebar Footer Styling */
        .sidebar-footer {
            position: fixed;
            bottom: 0;
            width: 18%;
            color: #555;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            background:#f9f9f9 /*#ffffff;  White background for readability */
            color: #333; 
            border-top: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- Header --------------------
st.markdown("<h1 class='main-title'>📄 PDF Summarizer</h1>", unsafe_allow_html=True)
st.markdown("""
    <p style="text-align: center; font-size: 18px; color: #555;">
        Extract and summarize PDF content effortlessly, get concise summaries in multiple languages.
    </p>
""", unsafe_allow_html=True)

# -------------------- PDF Upload --------------------
st.sidebar.markdown("<div class='sidebar-heading upload'>📂 Upload PDF</div>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Choose a PDF", type=["pdf"])

# -------------------- Language Selection --------------------
st.sidebar.markdown("<div class='sidebar-heading language'>🌐 Select Language</div>", unsafe_allow_html=True)
language = st.sidebar.selectbox(
    "Choose language for the summary",
    [
        "English", "French", "Spanish", "German", "Italian", "Hindi",
        "Chinese", "Japanese", "Russian",
        "Kannada", "Tamil", "Telugu", "Marathi", "Bengali", "Gujarati",
        "Malayalam", "Punjabi"
    ]
)

# Map language names to language codes
language_codes = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Hindi": "hi",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Russian": "ru",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Malayalam": "ml",
    "Punjabi": "pa"
}
language_code = language_codes[language]

# -------------------- PDF Text Extraction --------------------
def extract_text_with_pymupdf(pdf_path):
    """Extracts entire text from PDF using PyMuPDF."""
    pdf = fitz.open(pdf_path)
    full_text = ""

    for page in pdf:
        full_text += page.get_text()

    pdf.close()
    return full_text

# -------------------- Gemini Bilingual Summarization --------------------
def bilingual_summary(full_text, model="gemini-1.5-flash", max_tokens=8192, lang="en"):
    """Generates summary in both English and the selected language."""
    try:
        model = genai.GenerativeModel(model)

        # English summary
        english_response = model.generate_content(f"Summarize this content in English: {full_text}")
        english_summary = english_response.text

        # Selected language summary
        lang_response = model.generate_content(f"Summarize this content in {language} ({lang}): {full_text}")
        lang_summary = lang_response.text

        return english_summary, lang_summary

    except Exception as e:
        st.error(f"Error during summarization: {e}")
        return "", ""

# -------------------- Main Workflow --------------------
if uploaded_file is not None:
    pdf_path = "uploaded_file.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    full_text = extract_text_with_pymupdf(pdf_path)

    st.markdown("### 📚 Extracted PDF Content")
    with st.expander("📚 **View Extracted Text**", expanded=False):
        st.markdown(f"<div class='custom-box'>{full_text}</div>", unsafe_allow_html=True)

    if st.button("⚡ Generate Summary"):
        english_summary, lang_summary = bilingual_summary(full_text, lang=language_code)

        # Display summaries based on selected language
        if language_code == "en":
            # Only show English summary
            st.markdown("### ✍️ English Summary:")
            st.markdown(f"<div class='custom-box'>{english_summary}</div>", unsafe_allow_html=True)

            # Prepare download content (English only)
            summary_output = (
                f"📄 PDF Summarizer Output\n\n"
                f"### English Summary:\n{english_summary}"
            )

        else:
            # Show both English and translated summary
            st.markdown("### ✍️  Summary:")
            # st.markdown(f"### 🌍 {language} Summary:")
            st.markdown(f"<div class='custom-box'>{lang_summary}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='custom-box'>{english_summary}</div>", unsafe_allow_html=True)

           

            # Prepare download content (both summaries)
            summary_output = (
                f"📄 PDF Summarizer Output\n\n"
                f"### English Summary:\n{english_summary}\n\n"
                f"### {language} Summary:\n{lang_summary}"
            )

        # Add download button
        st.download_button(
            label="📥 Download Summaries",
            data=summary_output,
            file_name="PDF_Summary.txt",
            mime="text/plain"
        )

      
    # -------------------- Sidebar Footer --------------------
st.sidebar.markdown("""
    <div class='sidebar-footer'>
        🔥  API used <b>Google Gemini</b> <br> Developed by <i>Saumya Dwivedi </i>
    </div>
""", unsafe_allow_html=True)
