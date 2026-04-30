import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="HKBK AI Generator", page_icon="🎓")
st.title("🎯 Outcome-Aligned Lab & Quiz Generator")

# Inputs based on your Reference Image
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
            # 1. Setup Google AI directly (Bypasses LangChain 404 bug)
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 2. Build the prompt
            prompt = f"""
            Generate a Training Lab and Quiz for: {outcome}
            Bloom's Level: {bloom} | Difficulty: {diff}
            Include: Lab Steps, 5 Questions, and Answer Key.
            """
            
            with st.spinner("Generating with Gemini..."):
                # 3. Call the model directly
                response = model.generate_content(prompt)
                result_text = response.text
                
                st.success("Generation Complete!")
                st.markdown(result_text)
                
                # Export feature from your reference image
                st.download_button("Download for LMS", result_text, file_name="lab_module.txt")
                
        except Exception as e:
            st.error(f"Error: {e}")
