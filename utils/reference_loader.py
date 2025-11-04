import os
from utils.pdf_handler import extract_pdf_text

def load_reference_documents():
    """
    Load the 4 reference documents for FOI analysis from documents folder.
    Returns a dictionary with document names and their text content.
    """
    ref_docs = {}
    ref_dir = "documents"
    
    # Define the 4 reference documents (exact filenames from your GitHub)
    doc_files = {
        "FOI Guidelines Part I": "FOI-Guidelines-Part-I-Preliminary-version-2.pdf",
        "FOI Guidelines Part IV": "FOI-Guidelines-Draft-Part-IV-Exempt-documents-2.pdf",
        "TA Act": "TA Act.pdf",
        "About TAA": "About the Taxation Administration Act.pdf"
    }
    
    # Try to load each document
    for name, filename in doc_files.items():
        filepath = os.path.join(ref_dir, filename)
        
        if os.path.exists(filepath):
            # Open as file object for extract_pdf_text
            with open(filepath, 'rb') as f:
                text = extract_pdf_text(f)
                if text:
                    ref_docs[name] = text
                else:
                    print(f"⚠️ Could not extract text from: {name}")
        else:
            print(f"⚠️ Not found: {filepath}")
    
    return ref_docs

def get_reference_context(ref_docs, max_chars=8000):
    """
    Combine reference documents into a single context string.
    Truncates to fit within token limits.
    """
    if not ref_docs:
        return ""
    
    context = "REFERENCE DOCUMENTS FOR FOI ANALYSIS:\n\n"
    
    for name, text in ref_docs.items():
        # Take first portion of each document
        sample_size = max_chars // len(ref_docs)
        sample = text[:sample_size] if len(text) > sample_size else text
        context += f"--- {name} ---\n{sample}\n\n"
    
    return context
    