import streamlit as st
from .call_1_analyze import analyze_chunks
from .call_2_identify import identify_exemptions
from .call_3_match import match_provisions
from .call_4_reason import generate_reasoning
from .call_5_summarize import create_summary

def run_foi_analysis(client, chunks: list[str], exemption_types: list[str]) -> dict:
    """
    Run complete FOI analysis with 5 AI calls.
    Returns results dictionary with all findings.
    """
    
    st.header("🤖 AI Analysis (5 Calls)")
    progress = st.progress(0)
    
    try:
        # AI Call 1: Analyze chunks
        progress.progress(20)
        with st.spinner("🤖 Call 1/5: Analyzing document chunks..."):
            analysis = analyze_chunks(client, chunks)
        st.success("✅ Call 1 Complete")
        
        # AI Call 2: Identify exemptions
        progress.progress(40)
        with st.spinner("🤖 Call 2/5: Identifying exemptions..."):
            raw_exemptions = identify_exemptions(client, chunks, exemption_types)
        st.success(f"✅ Call 2 Complete: {len(raw_exemptions)} found")
        
        # AI Call 3: Match provisions
        progress.progress(60)
        with st.spinner("🤖 Call 3/5: Matching FOI provisions..."):
            matched = match_provisions(client, raw_exemptions)
        st.success("✅ Call 3 Complete")
        
        # AI Call 4: Generate reasoning
        progress.progress(80)
        with st.spinner("🤖 Call 4/5: Generating legal reasoning..."):
            final_exemptions = generate_reasoning(client, matched)
        st.success("✅ Call 4 Complete")
        
        # AI Call 5: Create summary
        progress.progress(90)
        with st.spinner("🤖 Call 5/5: Creating executive summary..."):
            summary = create_summary(client, final_exemptions)
        st.success("✅ Call 5 Complete")
        
        progress.progress(100)
        
        return {
            'analysis': analysis,
            'exemptions': final_exemptions,
            'summary': summary
        }
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

