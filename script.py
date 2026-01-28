import os
import streamlit as st
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from prompt_templates import SYSTEM_PROMPT,PRELEARNING_PROMPT, SCRIPT_GENERATION, VALIDATION_PROMPT

load_dotenv()

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

def generate_prelearning(cfg):
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.3)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("system", PRELEARNING_PROMPT),
        ("user", "{text}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"text": cfg["prelearning_words"]})


def generate_script(cfg):
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.2)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", SCRIPT_GENERATION)
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke(cfg)


def validate_script(script, cfg):
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.1)
    prompt = ChatPromptTemplate.from_messages([
        ("system", VALIDATION_PROMPT),
        ("user", "{script}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"script": script, **cfg})


def update_scenario_with_user_input(user_input):
    llm = ChatOpenAI(model="gpt-4.1-mini")
    scenario = st.session_state.scenario
    cfg = scenario["config"]
    current_script = scenario["script"]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("system", SCRIPT_GENERATION),
        ("system", """
            You are an interactive scenario editor.
            You must:
            - Understand the user's request
            - Decide whether user wants: explanation, partial rewrite, full regeneration
            - NEVER break constraints
            - ONLY modify requested parts
        """),
        ("user", """
            CURRENT SCRIPT:
            {script}

            USER MESSAGE:
            {user_input}

            CONFIG:
            Situation: {situation}
            Level: {level}
            Single response: {total_open_responses}
            MCQ: {total_mcq}
            Yes/No: {total_yes_no}

            Respond with updated script + explanation
        """)
    ])
    chain = prompt | llm | StrOutputParser()
    updated_script = chain.invoke({"script": current_script, "user_input": user_input, **cfg})

    st.session_state.scenario["script"] = updated_script
    st.session_state.messages.append({"role": "assistant", "content": updated_script})


def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "config" not in st.session_state:
        st.session_state.config = None
    if "scenario" not in st.session_state:
        st.session_state.scenario = None
    if "generated" not in st.session_state:
        st.session_state.generated = False


def run_generation():
    cfg = st.session_state.config

    prelearning_result = generate_prelearning(cfg)
    print("Prelearning done")
    st.session_state.messages.append({"role": "assistant", "content": prelearning_result})
    cfg = {
        **cfg,
        "prelearning_script": prelearning_result
    }
    raw_script = generate_script(cfg)
    print("Script generation done")
    st.session_state.messages.append({"role": "assistant", "content": raw_script})
    validated_script = validate_script(raw_script, cfg)
    print("Script validation done")
    st.session_state.scenario = {"script": validated_script, "config": cfg}
    st.session_state.messages.append({"role": "assistant", "content": validated_script})
    st.session_state.generated = True


def main():
    st.title("Script Generator")
    init_state()

    st.sidebar.header("Setup")
    situation = st.sidebar.text_input("Situation")
    prelearning_words = st.sidebar.text_area("Pre-Learning Words")
    num_mcq = st.sidebar.number_input("Number of Multiple Choice Questions", min_value=0, step=1)
    num_yes_no = st.sidebar.number_input("Number of Yes/No Questions", min_value=0, step=1)
    num_open_responses = st.sidebar.number_input("Number of Single Response Questions", min_value=0, step=1)
    level = st.sidebar.selectbox("English Level", ["Beginner", "Intermediate", "Advanced"])

    if st.sidebar.button("Submit"):
        st.session_state.config = {
            "situation": situation,
            "prelearning_words": prelearning_words,
            "total_mcq": num_mcq,
            "total_yes_no": num_yes_no,
            "total_open_responses": num_open_responses,
            "level": level,
        }
        st.session_state.messages = []
        run_generation()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Type your response here"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        if st.session_state.scenario:
            update_scenario_with_user_input(user_input)


if __name__ == "__main__":
    main()
