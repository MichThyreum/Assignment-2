import PyPDF2

def extract_pdf_text(uploaded_file) -> str:
    """Extract all text from uploaded PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return None

