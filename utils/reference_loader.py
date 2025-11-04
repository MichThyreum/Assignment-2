import os
from pathlib import Path
from utils.pdf_handler import extract_pdf_text
import streamlit as st

def load_reference_documents():
    ref_docs = {}
    
    # Since we're in utils/, go up one level to project root where documents is
    current_file = Path(__file__).resolve()
    utils_dir = current_file.parent
    project_root = utils_dir.parent
    
    # Absolute path to documents
    documents_dir = project_root / "documents"
    
    # DEBUG: Print what we're looking for
    st.sidebar.write("🔍 **Debug Info:**")
    st.sidebar.write(f"Current file: `{current_file}`")
    st.sidebar.write(f"Utils dir: `{utils_dir}`")
    st.sidebar.write(f"Project root: `{project_root}`")
    st.sidebar.write(f"Documents dir: `{documents_dir}`")
    st.sidebar.write(f"Documents exists: **{documents_dir.exists()}**")
    
    if documents_dir.exists():
        st.sidebar.write(f"Is directory: **{documents_dir.is_dir()}**")
        try:
            files_in_docs = list(documents_dir.iterdir())
            st.sidebar.write(f"Files found: **{len(files_in_docs)}**")
            for f in files_in_docs:
                st.sidebar.write(f"  - {f.name}")
        except Exception as e:
            st.sidebar.write(f"Error listing files: {e}")
    
    # Debug: Check if folder exists
    if not documents_dir.exists():
        st.sidebar.write("❌ Documents dir not found, trying alternates...")
        # Try alternate paths
        alt_paths = [
            Path.cwd() / "documents",
            Path("/workspaces/Assignment-2/documents"),
            project_root.parent / "documents"
        ]
        for alt in alt_paths:
            exists = alt.exists() and alt.is_dir()
            st.sidebar.write(f"  Trying: `{alt}` - **{exists}**")
            if exists:
                documents_dir = alt
                st.sidebar.write(f"✅ Using: `{documents_dir}`")
                break
    
    if not documents_dir.exists() or not documents_dir.is_dir():
        st.sidebar.write("❌ **No valid documents directory found**")
        st.sidebar.write(f"CWD: `{Path.cwd()}`")
        return {}
    
    # Exact filenames - FIXED to match your actual files
    doc_files = {
        "FOI Guidelines Part I": "FOI-Guidelines-Part-I-Preliminary-version-2.pdf",
        "FOI Guidelines Part IV": "FOI-Guidelines-Draft-Part-IV-Exempt-documents.pdf",
        "TA Act": "TA Act.pdf",
        "About TAA": "About the Taxation Administration Act.pdf"
    }
    
    st.sidebar.write("---")
    st.sidebar.write("📄 **Looking for files:**")
    
    # Load each document
    for name, filename in doc_files.items():
        filepath = documents_dir / filename
        exists = filepath.exists()
        st.sidebar.write(f"**{name}**")
        st.sidebar.write(f"  File: `{filename}`")
        st.sidebar.write(f"  Exists: **{exists}**")
        
        if filepath.exists():
            try:
                with open(filepath, 'rb') as f:
                    text = extract_pdf_text(f)
                    if text and len(text) > 100:
                        ref_docs[name] = text
                        st.sidebar.write(f"  ✅ Loaded ({len(text)} chars)")
                    else:
                        st.sidebar.write(f"  ❌ No text extracted")
            except Exception as e:
                st.sidebar.write(f"  ❌ Error: {e}")
        else:
            st.sidebar.write(f"  ❌ File not found")
    
    st.sidebar.write("---")
    st.sidebar.write(f"📚 **Total loaded: {len(ref_docs)}**")
    
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
    
    if "FOI Guidelines Part I" in ref_docs:
        context += "--- FOI Guidelines Part I (General Guide) ---\n"
        context += ref_docs["FOI Guidelines Part I"][:2000] + "\n\n"
    
    return context
    









    