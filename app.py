import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

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
            # Using the 'models/' prefix forces the correct path resolution
            llm = ChatGoogleGenerativeAI(
                model="models/gemini-1.5-flash", 
                google_api_key=st.secrets["GOOGLE_API_KEY"]
            )
           
            template = """
            Generate a Training Lab and Quiz for: {outcome}
            Bloom's Level: {bloom} | Difficulty: {diff}
            Include: Lab Steps, 5 Questions, and Answer Key.
            """
            
            prompt = PromptTemplate.from_template(template)
            chain = prompt | llm
            
            with st.spinner("Generating with Gemini..."):
                response = chain.invoke({"outcome": outcome, "bloom": bloom, "diff": diff})
                result_text = response.content
                
                st.success("Generation Complete!")
                st.markdown(result_text)
                
                # Export feature from your reference image
                st.download_button("Download for LMS", result_text, file_name="lab_module.txt")
                
        except Exception as e:
            st.error(f"Error calling the model: {e}")
