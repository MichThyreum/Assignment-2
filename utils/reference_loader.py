import os
from pathlib import Path
from utils.pdf_handler import extract_pdf_text

def load_reference_documents():
    ref_docs = {}
    
    # Get absolute path to documents folder relative to Home.py
    # Home.py is in the root, documents is also in the root
    home_file = Path(__file__).parent.parent / "Home.py"
    documents_dir = home_file.parent / "documents"
    
    if not documents_dir.exists() or not documents_dir.is_dir():
        return {}
    
    # Your actual filenames
    doc_files = {
        "FOI Guidelines Part IV": "FOI-Guidelines-Draft-Part-IV-Exempt-documents.pdf",
        "TA Act": "TA Act.pdf",
        "About TAA": "About the Taxation Administration Act.pdf"
    }
    
    # Load each document
    for name, filename in doc_files.items():
        filepath = documents_dir / filename
        
        if filepath.exists():
            try:
                with open(filepath, 'rb') as f:
                    text = extract_pdf_text(f)
                    if text and len(text) > 100:
                        ref_docs[name] = text
            except Exception:
                pass
    
    return ref_docs

def get_reference_context(ref_docs, max_chars=10000):
    if not ref_docs:
        return ""
    
    context = "REFERENCE DOCUMENTS:\n\n"
    
    if "FOI Guidelines Part IV" in ref_docs:
        context += "--- FOI Guidelines Part IV (PRIMARY - Victorian FOI Exemptions) ---\n"
        context += ref_docs["FOI Guidelines Part IV"][:4000] + "\n\n"
    
    if "TA Act" in ref_docs:
        context += "--- Taxation Administration Act (Sections 91, 92, 93) ---\n"
        context += ref_docs["TA Act"][:2000] + "\n\n"
    
    if "About TAA" in ref_docs:
        context += "--- About TAA (Context) ---\n"
        context += ref_docs["About TAA"][:2000] + "\n\n"
    
    return context
    

    

    









    