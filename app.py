import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

# 1. UI Setup
st.set_page_config(page_title="Outcome-Aligned Generator", layout="wide")
st.title("🎯 Outcome-Aligned Lab & Quiz Generator")

# 2. Sidebar Configuration (Inputs)
with st.sidebar:
    st.header("Project Parameters")
    outcome = st.text_area("Learning Outcome", "Explain REST API basics")
    bloom_level = st.selectbox("Bloom's Level", ["Apply", "Analyze", "Evaluate"])
    difficulty = st.select_slider("Difficulty", options=["Beginner", "Intermediate", "Advanced"])
    
    # Session Memory check
    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(memory_key="chat_history")

# 3. LangChain Logic (Prompt Templates)
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

template = """
You are an expert L&D Trainer. 
Outcome: {outcome}
Bloom's Level: {bloom_level}
Current Difficulty: {difficulty}

Generate:
1. A practical Lab Exercise.
2. A 5-question Quiz.
3. Detailed Model Answers and a Scoring Key.

{chat_history}
"""

prompt = PromptTemplate(input_variables=["outcome", "bloom_level", "difficulty", "chat_history"], template=template)

# Memory integration as per reference image
chain = LLMChain(llm=llm, prompt=prompt, memory=st.session_state.memory)

# 4. Execution
if st.button("Generate Training Content"):
    with st.spinner("Processing with LangChain..."):
        response = chain.run({"outcome": outcome, "bloom_level": bloom_level, "difficulty": difficulty})
        st.markdown("### Generated Training Lab & Quiz")
        st.info(response)
        
        # Simple Export to LMS (Mockup)
        st.download_button("Export to LMS (.txt)", response, file_name="training_module.txt")
        if st.button("Generate Training Content"):
    try:
        # Switching to 3.5-turbo is safer for student/free accounts
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        
        chain = LLMChain(llm=llm, prompt=prompt, memory=st.session_state.memory)
        
        with st.spinner("Generating content..."):
            response = chain.run({
                "outcome": outcome, 
                "bloom_level": bloom_level, 
                "difficulty": difficulty
            })
            st.success("Done!")
            st.markdown(response)
            
    except Exception as e:
        if "rate_limit_shaded" in str(e).lower() or "insufficient_quota" in str(e).lower():
            st.error("🚫 OpenAI Rate Limit Reached: Please check your API credits at platform.openai.com.")
        else:
            st.error(f"An error occurred: {e}")
