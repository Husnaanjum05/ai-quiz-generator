import streamlit as st
import google.generativeai as genai
from google.api_core import client_options

st.set_page_config(page_title="HKBK AI Generator", page_icon="🎓")
st.title("🎯 Outcome-Aligned Lab & Quiz Generator")

with st.sidebar:
    st.header("Settings")
    outcome = st.text_area("Learning Outcome", "Basics of Python Loops")
    bloom = st.selectbox("Bloom's Level", ["Apply", "Analyze", "Evaluate"])
    diff = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])

if st.button("Generate Training Materials"):
    if not st.secrets.get("GOOGLE_API_KEY"):
        st.error("Missing API Key in Streamlit Secrets!")
    else:
        try:
            # FORCE v1 API VERSION: This bypasses the v1beta 404 bug
            options = client_options.ClientOptions(api_endpoint="generativelanguage.googleapis.com")
            genai.configure(
                api_key=st.secrets["GOOGLE_API_KEY"],
                client_options=options
            )
            
            # Use the most generic model name
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Generate a {diff} Training Lab & 5-question Quiz for: {outcome} at Bloom's {bloom} level. Include model answers."
            
            with st.spinner("Processing..."):
                # Call with a forced versioning logic
                response = model.generate_content(prompt)
                
                st.success("Generation Complete!")
                st.markdown(response.text)
                st.download_button("Download Lab", response.text, file_name="lab.txt")
                
        except Exception as e:
            st.error(f"Final Fix Message: {e}")
