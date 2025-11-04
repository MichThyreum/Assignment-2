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
    layout="wide"
)

# Clean simple CSS
st.markdown("""
    <style>
    /* White background */
    .stApp {
        background-color: white;
    }
    
    /* All text black by default */
    .main * {
        color: #000000;
    }
    
    /* Headings in dark blue */
    h1, h2, h3, h4, h5, h6 {
        color: #1e3a8a !important;
    }
    
    /* Sidebar dark blue */
    [data-testid="stSidebar"] {
        background-color: #1e3a8a;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] input {
        color: #000000 !important;
        background-color: white !important;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #1e3a8a;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    
    .stButton button:hover {
        background-color: #1e40af;
    }
    
    /* Success/Info/Warning/Error boxes */
    .stSuccess, .stInfo, .stWarning, .stError {
        background-color: #f9fafb !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stSuccess *, .stInfo *, .stWarning *, .stError * {
        color: #000000 !important;
    }
    
    /* Make conclusion text RED */
    .conclusion-text {
        color: #dc2626 !important;
        font-weight: bold !important;
        font-size: 1.1em !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### 📋 Navigation")
    page = st.radio("", ["🏠 Home", "⚡ Analyzer", "📖 References"])

# Session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'num_customers' not in st.session_state:
    st.session_state.num_customers = 1

# PAGE 1: HOME
if page == "🏠 Home":
    st.title("🏛️ FOI Case Management Tool")
    st.divider()
    
    st.info("""
    **Welcome!** This tool analyzes documents for FOI exemptions.
    """)
    
    st.markdown("### 🚀 How It Works")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Enter Customer Names** 👥  
        Add up to 2 customer names
        
        **2. Upload Documents** 📂  
        Up to 2 PDF files
        
        **3. Analyze** 🔍  
        Click the analyze button
        """)
    
    with col2:
        st.markdown("""
        **4. Document Detection** 🎯  
        Identifies document types
        
        **5. FOI Analysis** ⚡  
        Documents analyzed for exemptions
        
        **6. Download Results** 💾  
        Export complete analysis
        """)
    
    st.divider()
    st.warning("⚠️ **Important:** This tool provides preliminary analysis only. Professional legal review required.")

# PAGE 2: ANALYZER
elif page == "⚡ Analyzer":
    st.title("⚡ FOI Document Analyzer")
    st.divider()
    
    # API Key
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🔑 API Key")
        
        show_key = st.checkbox("Show API key", value=False)
        
        if show_key:
            api_key = st.text_input("OpenAI API Key:", type="default")
        else:
            api_key = st.text_input("OpenAI API Key:", type="password")
        
        if api_key and api_key.startswith('sk-'):
            st.success("✅ Valid")
        elif api_key:
            st.error("❌ Invalid")
    
    if not api_key or not api_key.startswith('sk-'):
        st.warning("⚠️ Enter your OpenAI API key in the sidebar")
        st.stop()
    
    client = OpenAI(api_key=api_key)
    
    # Customer Names
    st.markdown("### 👥 Step 1: Customer Names")
    
    customer_names = []
    
    # Customer 1
    col1, col2 = st.columns(2)
    with col1:
        first_name_1 = st.text_input("Customer 1 - First Name", key="first_1")
    with col2:
        last_name_1 = st.text_input("Customer 1 - Last Name", key="last_1")
    
    if first_name_1 or last_name_1:
        customer_names.append(f"{first_name_1} {last_name_1}".strip())
    
    # Customer 2
    if st.session_state.num_customers >= 2 or st.checkbox("➕ Add second customer"):
        st.session_state.num_customers = 2
        col1, col2 = st.columns(2)
        with col1:
            first_name_2 = st.text_input("Customer 2 - First Name", key="first_2")
        with col2:
            last_name_2 = st.text_input("Customer 2 - Last Name", key="last_2")
        
        if first_name_2 or last_name_2:
            customer_names.append(f"{first_name_2} {last_name_2}".strip())
    
    st.divider()
    
    # Upload Documents
    st.markdown("### 📂 Step 2: Upload Documents (up to 2)")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if uploaded_files and len(uploaded_files) > 2:
        st.error("⚠️ Maximum 2 documents. Only first 2 will be analyzed.")
        uploaded_files = uploaded_files[:2]
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} document(s) uploaded")
        for idx, file in enumerate(uploaded_files, 1):
            st.caption(f"{idx}. {file.name}")
        
        # Clear button
        if st.button("🗑️ Clear Uploaded Documents"):
            st.session_state.clear()
            st.rerun()
    
    st.divider()
    
    # Analyze Button
    if st.button("🔍 Analyze Documents", type="primary", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one document")
        elif not customer_names:
            st.error("Please enter at least one customer name")
        else:
            all_results = []
            
            for idx, uploaded_file in enumerate(uploaded_files):
                st.markdown(f"### Analyzing: {uploaded_file.name}")
                
                is_letter_file = "letter" in uploaded_file.name.lower()
                
                with st.spinner("Extracting text..."):
                    text = extract_pdf_text(uploaded_file)
                
                if text:
                    st.success(f"✅ Extracted {len(text)} characters")
                    
                    addressed_to_customer = False
                    addressed_to = None
                    
                    for customer_name in customer_names:
                        if not customer_name:
                            continue
                        
                        first_name = customer_name.split()[0] if customer_name else ""
                        
                        patterns = [
                            f"Dear {customer_name}",
                            f"To: {customer_name}",
                            f"Dear {first_name}",
                        ]
                        
                        for pattern in patterns:
                            if pattern.lower() in text.lower():
                                addressed_to_customer = True
                                addressed_to = customer_name
                                break
                        
                        if addressed_to_customer:
                            break
                    
                    with st.spinner("Creating semantic chunks..."):
                        chunks = chunk_document(text)
                    st.success(f"✅ Created {len(chunks)} chunks")
                    
                    exemptions = [
                        "Tax Secrecy (TAA s 355)",
                        "Personal Privacy (s 47F)",
                        "Business/Commercial (s 47)"
                    ]
                    
                    analysis = run_foi_analysis(client, chunks, exemptions)
                    
                    if analysis:
                        num_exemptions = len(analysis.get('exemptions', []))
                        
                        if is_letter_file:
                            if addressed_to_customer:
                                conclusion = f"RELEASE IN FULL - Letter addressed to customer {addressed_to}"
                                note = f"This is a letter addressed to {addressed_to}."
                            else:
                                conclusion = "RELEASE IN FULL - Document is a letter"
                                note = "This document has 'letter' in its filename."
                        elif addressed_to_customer:
                            conclusion = f"RELEASE IN FULL - Addressed to customer {addressed_to}"
                            note = f"This document is addressed to {addressed_to}."
                        elif num_exemptions == 0:
                            conclusion = "RELEASE IN FULL - No exemptions identified"
                            note = "No FOI exemptions were found in this document."
                        elif num_exemptions <= 3:
                            conclusion = f"PARTIAL RELEASE - {num_exemptions} exemption(s) identified"
                            note = f"Document contains {num_exemptions} potential exemption(s). Review for redactions."
                        else:
                            conclusion = f"REVIEW REQUIRED - {num_exemptions} exemptions identified"
                            note = f"Document contains {num_exemptions} exemptions. Extensive review needed."
                        
                        result = {
                            "document_name": uploaded_file.name,
                            "is_letter_file": is_letter_file,
                            "addressed_to_customer": addressed_to_customer,
                            "addressed_to": addressed_to,
                            "conclusion": conclusion,
                            "note": note,
                            "summary": analysis.get('summary', ''),
                            "exemptions": analysis.get('exemptions', [])
                        }
                    else:
                        result = {
                            "document_name": uploaded_file.name,
                            "is_letter_file": is_letter_file,
                            "conclusion": "ERROR - Analysis failed",
                            "note": "Could not complete analysis",
                            "summary": "Analysis could not be completed",
                            "exemptions": []
                        }
                    
                    all_results.append(result)
                else:
                    st.error(f"Could not extract text from {uploaded_file.name}")
            
            st.session_state.results = all_results
            st.balloons()
            st.rerun()
    
    # Display Results
    if st.session_state.results:
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        
        for idx, result in enumerate(st.session_state.results, 1):
            st.markdown(f"### Document {idx}: {result['document_name']}")
            
            if result.get('is_letter_file'):
                st.info("✉️ This document has 'letter' in its filename")
            
            # Display conclusion in RED
            st.markdown(f'<p class="conclusion-text">{result["conclusion"]}</p>', unsafe_allow_html=True)
            
            if result.get('note'):
                st.caption(result['note'])
            
            with st.expander("📋 Executive Summary", expanded=True):
                st.markdown(result['summary'])
            
            if result['exemptions']:
                with st.expander(f"🔍 Exemptions ({len(result['exemptions'])})", expanded=False):
                    for ex_idx, ex in enumerate(result['exemptions'], 1):
                        st.markdown(f"**#{ex_idx} - {ex.get('type', 'Unknown')} ({ex.get('section', 'N/A')})**")
                        st.markdown(f"- Text: {ex.get('text', 'N/A')}")
                        st.markdown(f"- Reasoning: {ex.get('reasoning', 'N/A')}")
                        st.markdown(f"- Recommendation: {ex.get('recommendation', 'N/A')}")
                        st.caption(f"Confidence: {ex.get('confidence', 'Unknown')}")
                        st.divider()
            
            st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.download_button(
                "💾 Download Analysis (JSON)",
                json.dumps(st.session_state.results, indent=2),
                "foi_analysis.json",
                "application/json",
                use_container_width=True
            )
        with col2:
            if st.button("🔄 New", use_container_width=True):
                st.session_state.results = None
                st.session_state.num_customers = 1
                st.rerun()

# PAGE 3: REFERENCES
elif page == "📖 References":
    st.title("📖 Reference Documents")
    st.divider()
    
    st.markdown("""
    ### Legislation
    
    **Freedom of Information Act 1982 (Cth)**
    - Section 37 - Law enforcement
    - Section 47 - Public interest
    - Section 47E - Agency operations
    - Section 47F - Personal privacy
    
    **Taxation Administration Act 1953 (Cth)**
    - Section 355 - Taxpayer confidentiality
    
    ### How It Works
    
    1. **Document Detection**: 
       - Checks if filename contains "letter"
       - Checks if document is addressed to customer
    
    2. **Letter Handling**:
       - If filename contains "letter" → Analyzed but marked for full release
       - If addressed to customer → Analyzed but marked for full release
    
    3. **FOI Analysis** (5 AI steps):
       - Analyze document structure
       - Identify potential exemptions
       - Match against FOI Act
       - Generate legal reasoning
       - Create executive summary
    
    4. **Results**: Shows conclusion and detailed findings for each document
    
    ### Reference Documents
    
    📑 FOI Act.pdf  
    📋 FOI Guidelines  
    📜 Taxation Administration Act  
    📄 About the TAA  
    
    ---
    
    ⚠️ **Disclaimer**: Preliminary analysis only. Professional legal review required.
    """)

# Footer
st.markdown("---")
st.caption("⚖️ FOI Case Management Tool | For Internal Use Only")














        



