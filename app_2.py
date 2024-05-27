import os

import openai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

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
