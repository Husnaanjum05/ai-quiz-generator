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
        try:
            with st.spinner("Finding an active model in your account..."):
                # 1. Ask Google which models this specific API key can actually use
                list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
                list_res = requests.get(list_url).json()
                
                # Find the first model that supports "generateContent"
                available_models = [m['name'] for m in list_res.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
                
                if not available_models:
                    st.error("No models found. Please check if the 'Generative Language API' is enabled for this key.")
                else:
                    # Pick the best available model (prioritizing 1.5 flash or pro)
                    target_model = available_models[0]
                    for m in available_models:
                        if "gemini-1.5-flash" in m:
                            target_model = m
                            break
                    
                    st.info(f"Using active model: {target_model}")

                    # 2. Generate content using the discovered model path
                    gen_url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={api_key}"
                    prompt = f"Generate a {diff} Training Lab & 5-question Quiz for: {outcome} at Bloom's {bloom} level. Include answers."
                    payload = {"contents": [{"parts": [{"text": prompt}]}]}
                    
                    gen_res = requests.post(gen_url, json=payload)
                    gen_data = gen_res.json()

                    if gen_res.status_code == 200:
                        result_text = gen_data['candidates'][0]['content']['parts'][0]['text']
                        st.success("Generation Complete!")
                        st.markdown(result_text)
                        st.download_button("Download Lab", result_text, file_name="lab.txt")
                    else:
                        st.error(f"Generation Error: {gen_data.get('error', {}).get('message')}")
        
        except Exception as e:
            st.error(f"System Error: {e}")
