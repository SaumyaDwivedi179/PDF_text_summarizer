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
        /* Amazing Title with Custom Font */
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
            transition: transform 0.3s, box-shadow 0.5s;
            padding: 15px;
            border-radius: 12px;
            background:#454139;/*#ffffff;  */
             color:#faf7f0; 
        }
        .custom-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            background:background:#f9f9f9 /*#ffffff;  */
            # color:#454139;/*#ffffff;  */
            color:#faf7f0;
        }

        /* Buttons with Hover Effects */
        .stButton>button, .stDownloadButton>button {
            background: linear-gradient(135deg, #4CAF50, #2196F3);
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px 24px;
            transition: all 0.3s;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        .stButton>button:hover, .stDownloadButton>button:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }

        /* Sidebar Footer Styling */
        .sidebar-footer {
            position: fixed;
            bottom: 0;
            width: 18%;
            color: #faf7f0;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            background:#454139;
            border-top: 1px solid #ccc;
        }

        /* Why Section Styling */
        .why-section {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 40px 0;
        }

        .why-box {
            background: #454139;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            padding: 30px;
            transition: transform 0.3s, box-shadow 0.3s;
            text-align: center;
        }

        .why-box:hover {
            transform: translateY(-10px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
        }

        .why-icon {
            font-size: 50px;
            color: #4CAF50;
        }

        .why-title {
            font-size: 22px;
            font-weight: bold;
            color: #faf7f0;
            margin: 15px 0;
        }

        .why-description {
            font-size: 16px;
            color: #faf7f0;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- Header --------------------
st.markdown("<h1 class='main-title'>📄 PDF Summarizer</h1>", unsafe_allow_html=True)
st.markdown("""
    <p style="text-align: center; font-size: 18px; color: #656269;">
        Extract and summarize PDF content effortlessly, get concise summaries in multiple languages.
    </p>
""", unsafe_allow_html=True)

# # -------------------- Why to Use This App Section --------------------
st.markdown("""
    <div class="why-section">
        <div class="why-box">
            <div class="why-icon">⚡</div>
            <div class="why-title">Fast PDF Summarization</div>
            <div class="why-description">Quickly extract and summarize large PDFs into concise summaries.</div>
        </div>
          <div class="why-box">
            <div class="why-icon">🌐</div>
            <div class="why-title">Multilingual Support</div>
            <div class="why-description">Get summaries in multiple languages, including English, Hindi, Spanish, and more.</div>
        </div>
         <div class="why-box">
            <div class="why-icon">📥</div>
            <div class="why-title">Downloadable Summaries</div>
            <div class="why-description">Easily download your summarized content as a text file.</div>
        </div>

      
    </div>
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
    "English": "en", "French": "fr", "Spanish": "es", "German": "de",
    "Italian": "it", "Hindi": "hi", "Chinese": "zh-cn", "Japanese": "ja",
    "Russian": "ru", "Kannada": "kn", "Tamil": "ta", "Telugu": "te",
    "Marathi": "mr", "Bengali": "bn", "Gujarati": "gu",
    "Malayalam": "ml", "Punjabi": "pa"
}
language_code = language_codes[language]

# -------------------- PDF Text Extraction --------------------
def extract_text_with_pymupdf(pdf_path):
    pdf = fitz.open(pdf_path)
    full_text = "".join(page.get_text() for page in pdf)
    pdf.close()
    return full_text

def generate_summary(content, lang="en", length=500):
    """Generate summary in the specified language."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Summarize the following content in {lang} with approximately {length} words:\n\n"
            f"{content}"
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error during summarization: {e}")
        return ""

# -------------------- Main Workflow --------------------
if uploaded_file:
    pdf_path = "uploaded_file.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    full_text = extract_text_with_pymupdf(pdf_path)

    st.markdown("### 📚 Extracted PDF Content")
    with st.expander("📚 **View Extracted Text**"):
        st.write(full_text)

    # 🎯 Add Slider for Summary Length
    summary_length = st.slider(
        "🔧 Select Summary Length (in words)",
        min_value=200,
        max_value=1000,
        value=500,  # Default value
        step=50
    )

    if st.button("⚡ Generate Summary"):
        # Generate English summary
        english_summary = generate_summary(full_text, lang="en", length=summary_length)

        # Generate summary in the selected language (if different from English)
        if language != "English":
            translated_summary = generate_summary(full_text, lang=language_code, length=summary_length)

            # Display both summaries
            st.markdown(f"### ✍️  {language} Summary:")
            st.write(translated_summary)

            st.markdown("### ✍️ English Summary:")
            st.write(english_summary)

            

 # Combine both summaries for download
            combined_summary = (
                f"English Summary:\n\n{english_summary}\n\n"
                f"{language} Summary:\n\n{translated_summary}"
            )
            st.download_button("📥 Download Summary", combined_summary, file_name="summary.txt")

        else:
            # Display only English summary if language is English
            st.markdown("### ✍️ English Summary:")
            st.write(english_summary)

            # Download only English summary
            st.download_button("📥 Download Summary", english_summary, file_name="summary.txt")

# -------------------- Sidebar Footer --------------------
st.sidebar.markdown("""
    <div class='sidebar-footer'>
        🔥 API used: <b>Google Gemini</b> <br> Developed by: <i>Saumya Dwivedi</i>
    </div>
""", unsafe_allow_html=True)
