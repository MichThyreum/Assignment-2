import streamlit as st
from openai import OpenAI
from utils.pdf_handler import extract_pdf_text
from utils.chunker import chunk_document
from ai_calls.analyzer import run_foi_analysis
import json

# Page config
st.set_page_config(
    page_title="FOI Case Management Tool",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple modern CSS
st.markdown("""
    <style>
    /* Clean gradient background */
    .stApp {
        background: linear-gradient(to bottom right, #E3F2FD, #BBDEFB);
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* Text colors */
    * {
        color: #0D47A1 !important;
    }
    
    /* Modern buttons */
    .stButton button {
        background: #1976D2 !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem !important;
        border: none !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3) !important;
        transition: all 0.3s !important;
    }
    
    .stButton button:hover {
        background: #0D47A1 !important;
        box-shadow: 0 6px 16px rgba(13, 71, 161, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Clean sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #BBDEFB, #90CAF9);
    }
    
    /* Rounded corners for containers */
    .stExpander {
        background: white;
        border-radius: 10px;
        border: 1px solid #BBDEFB;
        margin: 0.5rem 0;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #1976D2;
    }
    
    /* Inputs */
    input, textarea, .stMultiSelect {
        border-radius: 8px !important;
        border: 2px solid #BBDEFB !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: #1976D2 !important;
    }
    
    /* Download button */
    .stDownloadButton button {
        background: #43A047 !important;
        border-radius: 10px !important;
    }
    
    /* Cards */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### 📋 Navigation")
    page = st.radio(
        "",
        ["🏠 How to Use", "📄 Document Analyzer", "📚 Reference Documents"]
    )

# Session state
if 'results' not in st.session_state:
    st.session_state.results = None

# PAGE 1: HOW TO USE
if page == "🏠 How to Use":
    st.title("🏛️ FOI Case Management Tool")
    st.divider()
    
    st.info("""
    **Welcome!** This tool helps you efficiently manage Freedom of Information (FOI) requests. 
    Use it for analyzing documents related to customer FOI requests including correspondence, 
    emails, investigation records, and other relevant documents.
    """)
    
    st.markdown("### 🚀 How to Use")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Go to Document Analyzer**  
        Click the tab in the sidebar
        
        **2. Enter API Key**  
        Provide your OpenAI API key
        
        **3. Upload PDF**  
        Upload the document to analyze
        """)
    
    with col2:
        st.markdown("""
        **4. Select Exemptions**  
        Choose exemption types to check
        
        **5. Analyze**  
        Click the analyze button
        
        **6. Review & Download**  
        Review results and export JSON
        """)
    
    st.divider()
    
    st.warning("⚠️ **Important:** This tool provides preliminary analysis only. All FOI decisions must be reviewed by qualified legal professionals.")
    
    st.success("🔒 **Privacy:** Your API key and documents are only used during your session and are not stored.")

# PAGE 2: DOCUMENT ANALYZER
elif page == "📄 Document Analyzer":
    st.title("📄 FOI Document Analyzer")
    st.divider()
    
    # API Key in sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🔑 API Key")
        
        api_key = st.text_input("OpenAI API Key:", type="password")
        
        if api_key and api_key.startswith('sk-'):
            st.success("✅ Key valid")
        elif api_key:
            st.error("❌ Invalid format")
        else:
            st.info("Enter your API key")
    
    if not api_key or not api_key.startswith('sk-'):
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar.")
        st.stop()
    
    client = OpenAI(api_key=api_key)
    
    # Upload
    st.markdown("### 📄 Step 1: Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
    
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name}")
        
        # Select exemptions
        st.markdown("### 🔍 Step 2: Select Exemptions")
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
        
        # Analyze
        if st.button("🚀 Analyze Document", type="primary", use_container_width=True):
            if not exemptions:
                st.error("Select at least one exemption category")
            else:
                with st.spinner("Extracting text..."):
                    text = extract_pdf_text(uploaded_file)
                
                if text:
                    st.success(f"✅ Extracted {len(text)} characters")
                    
                    with st.spinner("Creating chunks..."):
                        chunks = chunk_document(text)
                    st.success(f"✅ Created {len(chunks)} chunks")
                    
                    results = run_foi_analysis(client, chunks, exemptions)
                    
                    if results:
                        st.session_state.results = results
                        st.balloons()
                        st.rerun()
    
    # Display results
    if st.session_state.results:
        results = st.session_state.results
        
        st.markdown("---")
        st.markdown("## 📊 Results")
        
        # Summary
        st.markdown("### 📋 Executive Summary")
        st.info(results['summary'])
        
        st.markdown("---")
        
        # Exemptions
        st.markdown(f"### 🔍 Found {len(results['exemptions'])} Exemptions")
        
        if results['exemptions']:
            for idx, ex in enumerate(results['exemptions'], 1):
                with st.expander(f"#{idx} - {ex.get('type', 'Unknown')} ({ex.get('section', 'N/A')})"):
                    st.markdown(f"**Text:** {ex.get('text', 'N/A')}")
                    st.markdown(f"**Reasoning:** {ex.get('reasoning', 'N/A')}")
                    st.markdown(f"**Recommendation:** {ex.get('recommendation', 'N/A')}")
                    st.caption(f"Confidence: {ex.get('confidence', 'Unknown')}")
        else:
            st.info("No exemptions identified")
        
        # Download
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.download_button(
                "📥 Download Analysis (JSON)",
                json.dumps(results, indent=2),
                f"foi_analysis_{uploaded_file.name}.json",
                "application/json",
                use_container_width=True
            )
        with col2:
            if st.button("🔄 New Analysis", use_container_width=True):
                st.session_state.results = None
                st.rerun()

# PAGE 3: REFERENCE DOCUMENTS
elif page == "📚 Reference Documents":
    st.title("📚 Reference Documents")
    st.divider()
    
    st.markdown("""
    ### Primary Legislation
    
    #### Freedom of Information Act 1982 (Cth)
    The FOI Act provides access rights to government documents.
    
    **Key Sections:**
    - Section 37 - Law enforcement
    - Section 38 - Secrecy provisions  
    - Section 47 - Public interest
    - Section 47E - Agency operations
    - Section 47F - Personal privacy
    
    [View on legislation.gov.au](https://www.legislation.gov.au/Series/C2004A02562)
    
    ---
    
    #### Taxation Administration Act 1953 (Cth)
    Contains taxpayer confidentiality provisions.
    
    **Key Section:**
    - Section 355 - Taxpayer information confidentiality
    
    [View on legislation.gov.au](https://www.legislation.gov.au/Series/C1953A00001)
    
    ---
    
    ### Guidelines
    
    #### FOI Guidelines (OAIC)
    Official guidance on applying the FOI Act.
    
    - Part I: Preliminary  
    - Part IV: Exempt documents
    
    [View on oaic.gov.au](https://www.oaic.gov.au/freedom-of-information/foi-guidelines)
    
    ---
    
    ### How This Tool Uses These Documents
    
    The AI analyzes documents against these legislative provisions to:
    1. Identify potential exemptions
    2. Match text to statutory provisions
    3. Apply relevant legal tests
    4. Provide recommendations
    
    ⚠️ **Important:** This tool references legislation but is not a substitute for legal advice.
    
    ---
    
    ### Documents in Tool
    
    📄 FOI Act.pdf  
    📄 FOI Guidelines Part I  
    📄 FOI Guidelines Part IV  
    📄 Taxation Administration Act  
    📄 About the TAA
    """)

# Footer
st.markdown("---")
st.caption("⚖️ FOI Case Management Tool | For Internal Use Only | Professional legal review required")

        



