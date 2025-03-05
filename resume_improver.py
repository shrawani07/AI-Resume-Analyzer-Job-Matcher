import pdfplumber
import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip() if text.strip() else "⚠️ No text extracted!"
    except Exception as e:
        return f"⚠️ Error extracting text: {e}"

def improve_resume(resume_text):
    """Use AI to improve the resume."""
    prompt = f"""
    Improve the following resume by enhancing the structure, wording, and highlighting key achievements.
    Make it ATS-friendly and well-formatted.

    Resume:
    {resume_text}
    """

    try:
        # ✅ Corrected: Instantiate model before using `.generate_content()`
        model = genai.GenerativeModel("gemini-1.5-flash") 
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"⚠️ AI Improvement Error: {e}")
        return "Error generating improved resume."


def save_resume_as_pdf(text, filename="improved_resume.pdf"):
    """Save improved resume as a PDF file with UTF-8 encoding support."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # ✅ Replace non-ASCII characters with safe alternatives
    safe_text = text.encode("latin-1", "ignore").decode("latin-1")

    for line in safe_text.split("\n"):
        pdf.cell(200, 10, txt=line.encode("latin-1", "ignore").decode("latin-1"), ln=True, align='L')

    pdf.output(filename, "F")
    return filename

