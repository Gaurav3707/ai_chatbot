import streamlit as st
import requests
import logging, os, time
from decouple import config
import google.generativeai as genai

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the API key and endpoint for the Gemini LLM API
API_KEY = config('api_key')
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to send a message to the Gemini LLM
def get_hf_ai_response(user_message):

    try:
        response = response = model.generate_content(user_message)
        
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send message to Gemini API: {e}")
        return "Error processing your request, please try again."

# Function to send a message to the assistant
def send_message(msg_thread):
    try:
        # Join the messages into a single thread for context
        user_message = "\n".join([msg["content"] for msg in msg_thread if msg["role"] == "user"])
        response_content = get_hf_ai_response(user_message)
        logging.info(f"Sending Message Response: {response_content}")
        return response_content
    except Exception as e:
        logging.error(f"Failed to process message: {e}")
        return "Error processing your request, please try again."

st.title("AI Chatbot")
st.caption("Powered by Gemini")

# Display conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user input for ongoing conversation
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    user_msg_placeholder = st.chat_message("user").write(prompt)

    # Placeholder for the assistant's response
    assistant_response_placeholder = st.empty()
    response = send_message(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Display the data or results
st.write("To refresh press R")
