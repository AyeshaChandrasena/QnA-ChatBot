from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response  # Fixed typo here

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Input field
user_input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and user_input:
    response = get_gemini_response(user_input)

    # Add user query to chat history
    st.session_state["chat_history"].append(("You", user_input))

    st.subheader("The response is:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state["chat_history"].append(("Bot", chunk.text))

    # Display chat history
    st.subheader("The Chat History is:")
    for role, text in st.session_state["chat_history"]:
        st.write(f"**{role}:** {text}")
