import os

import openai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message

load_dotenv()

# Load the Excel file
df = pd.read_excel("staffing_info_extended.xlsx")

# Set your OpenAI API key
openai.api_key = os.environ.get("OPEN_AI_KEY")


# Function to create a response based on the question and the data
def get_staffing_recommendation(question, history):
    data = df.to_string(index=False)
    messages = [
        {
            "role": "system",
            "content": f"You are a staffing assistant. Given the following data about people:\n\n{data}",
        },
        {
            "role": "user",
            "content": f"The conversation so far:\n{history}\n\nAnswer the following question: {question}",
        },
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response.choices[0].message.content.strip()


# Streamlit app
st.title("Staffing MatchMaker")

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state["history"] = ""

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

# User input
question = st.chat_input("Ask a question about staffing...")


if question:
    with st.spinner("Generating response.."):
        response = get_staffing_recommendation(question, st.session_state["history"])
        st.session_state["user_prompt_history"].append(question)
        st.session_state["chat_answers_history"].append(response)

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(user_query, is_user=True)
        message(generated_response)
