import streamlit as st
from openai import OpenAI
from utils.pdf_handler import extract_pdf_text
from utils.chunker import chunk_document
from ai_calls.analyzer import run_foi_analysis
from openai_credentials import sidebar_api_key_configuration

# Page config
st.set_page_config(page_title="FOI Analyzer", page_icon="📋", layout="wide")

# API Key
api_key = sidebar_api_key_configuration()
if not api_key:
    st.warning("⚠️ Please enter your OpenAI API key in the sidebar.")
    st.stop()

client = OpenAI(api_key=api_key)

# Session state
if 'results' not in st.session_state:
    st.session_state.results = None

# Header
st.title("🏛️ FOI Document Analyzer")
st.markdown("Analyzes tax documents for Freedom of Information Act exemptions")
st.divider()

# Step 1: Upload
st.header("📄 Step 1: Upload Document")
uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])

if uploaded_file:
    st.success(f"✅ Uploaded: {uploaded_file.name}")
    
    # Step 2: Select exemptions
    st.header("🔍 Step 2: Select Exemption Categories")
    exemptions = st.multiselect(
        "Choose exemption types:",
        [
            "Business/Commercial (s 47)",
            "Personal Privacy (s 47F)",
            "Agency Operations (s 47E)",
            "Law Enforcement (s 37)",
            "Tax Secrecy (TAA s 355)"
        ],
        default=["Business/Commercial (s 47)", "Personal Privacy (s 47F)"]
    )
    
    # Analyze button
    if st.button("🚀 Analyze Document", type="primary"):
        if not exemptions:
            st.error("Please select at least one exemption category")
        else:
            # Extract text
            with st.spinner("Extracting text..."):
                text = extract_pdf_text(uploaded_file)
            
            if text:
                st.success(f"✅ Extracted {len(text)} characters")
                
                # Chunk document
                with st.spinner("Chunking document..."):
                    chunks = chunk_document(text)
                st.success(f"✅ Created {len(chunks)} semantic chunks")
                
                # Run AI analysis (5 calls)
                results = run_foi_analysis(client, chunks, exemptions)
                
                if results:
                    st.session_state.results = results
                    st.balloons()
                    st.rerun()

# Display results
if st.session_state.results:
    results = st.session_state.results
    
    st.header("📊 Results")
    
    # Summary
    st.subheader("Executive Summary")
    st.markdown(results['summary'])
    
    st.divider()
    
    # Exemptions
    st.subheader(f"🔍 Exemptions Found: {len(results['exemptions'])}")
    
    for idx, ex in enumerate(results['exemptions'], 1):
        with st.expander(f"{idx}. {ex['type']} - {ex['section']}"):
            st.info(f"**Text:** {ex['text']}")
            st.markdown(f"**Reasoning:** {ex['reasoning']}")
            st.markdown(f"**Recommendation:** {ex['recommendation']}")
            st.caption(f"Confidence: {ex['confidence']}")
    
    # Download
    st.divider()
    import json
    st.download_button(
        "📥 Download JSON",
        json.dumps(results, indent=2),
        f"foi_analysis_{uploaded_file.name}.json",
        "application/json"
    )
    
    if st.button("🔄 New Analysis"):
        st.session_state.results = None
        st.rerun()
        
