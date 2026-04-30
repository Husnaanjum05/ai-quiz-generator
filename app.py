import streamlit as st
import requests
import json

st.set_page_config(page_title="HKBK AI Generator", page_icon="🎓")
st.title("🎯 Outcome-Aligned Lab & Quiz Generator")

with st.sidebar:
    st.header("Settings")
    outcome = st.text_area("Learning Outcome", "Explain Python Loops")
    bloom = st.selectbox("Bloom's Level", ["Apply", "Analyze", "Evaluate"])
    diff = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])

if st.button("Generate Training Materials"):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("Missing API Key in Streamlit Secrets!")
    else:
        # SWITCHED TO GEMINI-PRO: This model is the most stable across all API versions
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        prompt = f"Generate a {diff} Training Lab & 5-question Quiz for: {outcome} at Bloom's {bloom} level. Include answers."
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        try:
            with st.spinner("Connecting to Stable Model..."):
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                response_data = response.json()

                if response.status_code == 200:
                    result_text = response_data['candidates'][0]['content']['parts'][0]['text']
                    st.success("Generation Complete!")
                    st.markdown(result_text)
                    st.download_button("Download Lab", result_text, file_name="lab.txt")
                else:
                    # If gemini-pro also fails, it's a regional/project restriction
                    st.error(f"Error {response.status_code}: {response_data.get('error', {}).get('message', 'Unknown Error')}")
        
        except Exception as e:
            st.error(f"Connection Error: {e}")
