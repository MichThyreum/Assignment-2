import streamlit as st
from openai import OpenAI
from utils.pdf_handler import extract_pdf_text
from utils.chunker import chunk_document
from ai_calls.analyzer import run_foi_analysis
from utils.reference_loader import load_reference_documents, get_reference_context
import json

st.set_page_config(page_title="FOI Case Management Tool", page_icon="🏛️", layout="wide")

# Simple CSS
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .main * { color: #000000; }
    h1, h2, h3 { color: #1e3a8a !important; }
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] input { color: #000000 !important; background-color: white !important; }
    .stButton button { background-color: #1e3a8a; color: white !important; }
    .conclusion { color: #dc2626 !important; font-weight: bold !important; font-size: 1.1em !important; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📋 Navigation")
    page = st.radio("", ["🏠 Home", "⚡ Analyzer", "📖 References"])
    
    if page == "⚡ Analyzer":
        st.markdown("---\n### 🔑 API Key")
        show_key = st.checkbox("Show API key")
        api_key = st.text_input("OpenAI API Key:", type="default" if show_key else "password")

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None

# PAGE 1: HOME
if page == "🏠 Home":
    st.title("🏛️ FOI Case Management Tool")
    st.divider()
    st.info("**Welcome!** This tool analyzes documents for FOI exemptions using reference legislation and guidelines.")
    
    st.markdown("### 🚀 How It Works")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**1. Enter Customer Names** 👥\n\n**2. Upload Documents** 📂\n\n**3. Analyze** 🔍")
    with col2:
        st.markdown("**4. Document Detection** 🎯\n\n**5. FOI Analysis** ⚡\n\n**6. Download Results** 💾")
    
    st.divider()
    st.warning("⚠️ **Important:** Preliminary analysis only. Professional legal review required.")

# PAGE 2: ANALYZER
elif page == "⚡ Analyzer":
    st.title("⚡ FOI Document Analyzer")
    st.divider()
    
    # Check API key
    if not api_key or not api_key.startswith('sk-'):
        st.warning("⚠️ Enter your OpenAI API key in the sidebar")
        st.stop()
    
    client = OpenAI(api_key=api_key)
    
    # Step 1: Customer Names
    st.markdown("### 👥 Step 1: Customer Names")
    col1, col2 = st.columns(2)
    first_1 = col1.text_input("Customer 1 - First Name", key="f1")
    last_1 = col2.text_input("Customer 1 - Last Name", key="l1")
    
    customer_names = [f"{first_1} {last_1}".strip()] if (first_1 or last_1) else []
    
    if st.checkbox("➕ Add second customer"):
        col1, col2 = st.columns(2)
        first_2 = col1.text_input("Customer 2 - First Name", key="f2")
        last_2 = col2.text_input("Customer 2 - Last Name", key="l2")
        if first_2 or last_2:
            customer_names.append(f"{first_2} {last_2}".strip())
    
    st.divider()
    
    # Step 2: Upload
    st.markdown("### 📂 Step 2: Upload Documents (up to 2)")
    files = st.file_uploader("Choose PDF files", type=['pdf'], accept_multiple_files=True)
    
    if files:
        files = files[:2]  # Limit to 2
        st.success(f"✅ {len(files)} document(s) uploaded")
        for i, f in enumerate(files, 1):
            st.caption(f"{i}. {f.name}")
        if st.button("🗑️ Clear"):
            st.session_state.clear()
            st.rerun()
    
    st.divider()
    
    # Analyze
    if st.button("🔍 Analyze Documents", type="primary", use_container_width=True):
        if not files:
            st.error("Please upload at least one document")
        elif not customer_names:
            st.error("Please enter at least one customer name")
        else:
            # Load reference documents
            st.info("📚 Loading reference documents...")
            ref_docs = load_reference_documents()
            
            if ref_docs:
                st.success(f"✅ Loaded {len(ref_docs)} reference documents")
            else:
                st.warning("⚠️ No reference documents found. Analysis will proceed without references.")
            
            results = []
            
            for file in files:
                st.markdown(f"### Analyzing: {file.name}")
                
                # Extract text
                text = extract_pdf_text(file)
                if not text:
                    st.error(f"Could not extract text from {file.name}")
                    continue
                
                st.success(f"✅ Extracted {len(text)} characters")
                
                # Check if letter
                is_letter = "letter" in file.name.lower()
                
                # Check if addressed to customer
                addressed_to = None
                for name in customer_names:
                    if not name:
                        continue
                    first = name.split()[0]
                    if any(p.lower() in text.lower() for p in [f"Dear {name}", f"To: {name}", f"Dear {first}"]):
                        addressed_to = name
                        break
                
                # Chunk and analyze
                chunks = chunk_document(text)
                st.success(f"✅ Created {len(chunks)} chunks")
                
                # Define exemptions based on reference documents
                exemptions = [
                    "Tax Secrecy (TAA s 355)",
                    "Personal Privacy (s 47F)",
                    "Business/Commercial (s 47)"
                ]
                
                # Get reference context
                ref_context = get_reference_context(ref_docs) if ref_docs else ""
                
                # Run analysis with reference documents
                analysis = run_foi_analysis(client, chunks, exemptions, ref_context)
                
                if analysis:
                    num_ex = len(analysis.get('exemptions', []))
                    
                    # Determine conclusion
                    if is_letter:
                        conclusion = f"RELEASE IN FULL - Letter addressed to {addressed_to}" if addressed_to else "RELEASE IN FULL - Document is a letter"
                    elif addressed_to:
                        conclusion = f"RELEASE IN FULL - Addressed to {addressed_to}"
                    elif num_ex == 0:
                        conclusion = "RELEASE IN FULL - No exemptions"
                    elif num_ex <= 3:
                        conclusion = f"PARTIAL RELEASE - {num_ex} exemption(s)"
                    else:
                        conclusion = f"REVIEW REQUIRED - {num_ex} exemptions"
                    
                    results.append({
                        "document_name": file.name,
                        "conclusion": conclusion,
                        "summary": analysis.get('summary', ''),
                        "exemptions": analysis.get('exemptions', [])
                    })
            
            st.session_state.results = results
            st.balloons()
            st.rerun()
    
    # Display Results
    if st.session_state.results:
        st.markdown("---\n## 📊 Analysis Results")
        
        for i, r in enumerate(st.session_state.results, 1):
            st.markdown(f"### Document {i}: {r['document_name']}")
            st.markdown(f'<p class="conclusion">{r["conclusion"]}</p>', unsafe_allow_html=True)
            
            with st.expander("📋 Executive Summary", expanded=True):
                st.markdown(r['summary'])
            
            if r['exemptions']:
                with st.expander(f"🔍 Exemptions ({len(r['exemptions'])})", expanded=False):
                    for j, ex in enumerate(r['exemptions'], 1):
                        st.markdown(f"**#{j} - {ex.get('type', 'Unknown')} ({ex.get('section', 'N/A')})**")
                        st.markdown(f"- Text: {ex.get('text', 'N/A')}")
                        st.markdown(f"- Reasoning: {ex.get('reasoning', 'N/A')}")
                        st.markdown(f"- Recommendation: {ex.get('recommendation', 'N/A')}")
                        st.caption(f"Confidence: {ex.get('confidence', 'Unknown')}")
                        st.divider()
            
            st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        col1.download_button("💾 Download Analysis (JSON)", json.dumps(st.session_state.results, indent=2), 
                            "foi_analysis.json", "application/json", use_container_width=True)
        if col2.button("🔄 New", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# PAGE 3: REFERENCES
else:
    st.title("📖 Reference Documents")
    st.divider()
    st.markdown("""
    ### Legislation & Guidelines
    
    **Freedom of Information Act 1982 (Cth)**
    - Section 47 - Public interest
    - Section 47E - Agency operations
    - Section 47F - Personal privacy
    
    **Taxation Administration Act 1953 (Cth)**
    - Section 355 - Taxpayer confidentiality
    
    ### Reference Documents Used in Analysis
    
    This tool uses the following documents to analyze FOI exemptions:
    
    📋 **FOI Guidelines Part I - Preliminary (Version 2)**  
    Overview of FOI framework and fundamental principles
    
    📑 **FOI Guidelines Draft Part IV - Exempt Documents (Version 2)**  
    Detailed guidance on exemption categories and application
    
    📜 **Taxation Administration Act 1953**  
    Complete legislation including Section 355 (taxpayer secrecy)
    
    📄 **About the Taxation Administration Act**  
    Explanatory guide on TAA provisions and interpretations
    
    ### How It Works
    
    1. **Document Detection** - Checks filename and content for letters
    2. **Letter Handling** - Letters to customers marked for full release
    3. **FOI Analysis** - 5 AI analysis steps using reference documents:
       - Analyze document structure and content
       - Identify potential exemptions
       - Match against FOI provisions
       - Generate legal reasoning
       - Create executive summary
    4. **Results** - Provides conclusion with detailed findings
    
    ---
    
    ⚠️ **Disclaimer:** Preliminary analysis only. Professional legal review required.
    """)

st.markdown("---")
st.caption("⚖️ FOI Case Management Tool | For Internal Use Only")

















        



