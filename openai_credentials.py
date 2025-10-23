"""
OpenAI API Credentials Sidebar Module
Based on: https://github.com/stoneman-mls/openai_credentials
"""

import streamlit as st


def sidebar_api_key_configuration() -> str:
    """
    Configures the OpenAI API key through the Streamlit sidebar.
    
    Returns:
        str: The API key if provided, None otherwise
    """
    with st.sidebar:
        st.header("🔑 API Configuration")
        
        st.markdown("""
        ### OpenAI API Key Required
        
        This application requires an OpenAI API key to function.
        
        **How to get your API key:**
        1. Go to [OpenAI Platform](https://platform.openai.com/)
        2. Sign in or create an account
        3. Navigate to API Keys section
        4. Create a new secret key
        5. Copy and paste it below
        
        **Note:** Your API key is not stored and only used for this session.
        """)
        
        api_key = st.text_input(
            "Enter your OpenAI API Key:",
            type="password",
            help="Your API key will only be used for this session"
        )
        
        if api_key:
            if api_key.startswith('sk-'):
                st.success("✅ API Key provided")
                return api_key
            else:
                st.error("❌ Invalid API key format. Should start with 'sk-'")
                return None
        else:
            st.info("👆 Please enter your API key above to continue")
            return None


if __name__ == "__main__":
    # Test the module
    key = sidebar_api_key_configuration()
    if key:
        st.write("API Key configured successfully!")
    else:
        st.write("No API key provided yet.")
        
