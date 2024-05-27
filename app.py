import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import ChatPrompt

load_dotenv()


# Load the Excel file
df = pd.read_excel("staffing_info_extended.xlsx")

# Initialize the OpenAI LLM
llm = OpenAI(api_key=os.environ.get("OPEN_AI_KEY"), model="gpt-3.5-turbo")

# Define a prompt template
prompt_template = ChatPrompt(
    "You are a staffing assistant. Given the following data about people:\n\n{data}\n\nThe conversation so far:\n{history}\n\nAnswer the following question: {question}"
)


# Function to create a response based on the question and the data
def get_staffing_recommendation(question, history):
    data = df.to_string(index=False)
    prompt = prompt_template.format(data=data, history=history, question=question)
    response = llm(prompt)
    return response


# Streamlit app
st.title("Staffing Chatbot")

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state["history"] = ""

# User input
question = st.text_input("Ask a question about staffing:")

if st.button("Send"):
    if question:
        # Get the response from the agent
        response = get_staffing_recommendation(question, st.session_state["history"])

        # Update chat history
        st.session_state["history"] += f"User: {question}\nBot: {response}\n"

        # Display chat history
        st.text_area("Chat History", value=st.session_state["history"], height=400)

        # Clear the input box
        st.text_input("Ask a question about staffing:", value="", key="new")
