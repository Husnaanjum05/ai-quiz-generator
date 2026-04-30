import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="HKBK AI Generator", page_icon="🎓")
st.title("🎯 Outcome-Aligned Lab & Quiz Generator")

# Sidebar based on your Reference Image (image_28865c.png)
with st.sidebar:
    st.header("Settings")
    outcome = st.text_area("Learning Outcome", "Explain Cloud Computing basics")
    bloom = st.selectbox("Bloom's Level", ["Apply", "Analyze", "Evaluate"])
    diff = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])

if st.button("Generate Training Materials"):
    if not st.secrets.get("GOOGLE_API_KEY"):
        st.error("Missing API Key in Streamlit Secrets!")
    else:
        try:
            # 1. Direct configuration
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            # 2. Use the version-agnostic model call
            # This is the secret fix for the v1beta 404 error
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash-latest'
            )
            
            prompt = f"Generate a {diff} level Training Lab and 5-question Quiz for: {outcome} at Bloom's {bloom} level. Include scoring keys."
            
            with st.spinner("Generating..."):
                # Use the 'stream' parameter to handle connection better
                response = model.generate_content(prompt)
                
                if response:
                    st.success("Generation Complete!")
                    st.markdown(response.text)
                    
                    # Download button as per project requirement
                    st.download_button("Download as Text", response.text, file_name="lab.txt")
                
        except Exception as e:
            # Helpful error message for the demo
            st.error(f"System Message: {e}")
