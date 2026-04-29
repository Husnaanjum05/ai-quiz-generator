import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate content
def generate_content(outcome, level):
    prompt = f"""
    Generate a training lab and quiz based on:
    Learning Outcome: {outcome}
    Difficulty Level: {level}

    Include:
    1. Lab Task
    2. 3 Quiz Questions
    3. Answers
    4. Scoring Key
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output[0].content[0].text

# Streamlit UI
st.set_page_config(page_title="AI Quiz Generator")

st.title("🎯 AI Training Lab & Quiz Generator")

outcome = st.text_input("Enter Learning Outcome")
level = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])

if st.button("Generate"):
    if outcome:
        result = generate_content(outcome, level)
        st.write(result)
    else:
        st.warning("Please enter a learning outcome")
