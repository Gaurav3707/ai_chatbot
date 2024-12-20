import streamlit as st
import requests
import logging, os, time
from decouple import config
from langchain_google_genai import ChatGoogleGenerativeAI
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


os.environ["GOOGLE_API_KEY"] = config('api_key')
llm = ChatGoogleGenerativeAI(model="gemini-pro",convert_system_message_to_human=True)


def get_hf_ai_response(user_message):
    return llm.invoke(user_message)



# Function to send a message to the assistant
def send_message(msg_thread):
    try:
        response = get_hf_ai_response(msg_thread)
        print(f"Sending Message Response: {response}")
        print(response.content)
        return response.content
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send message: {e}")
        return "Error processing your request, please try again."

# Sidebar for user input
# with st.sidebar:
    # user_id = st.text_input("User ID", key="user_id", type="default")
    # new_user_id = st.text_input("New User ID", key="new_user_id", type="default")
    # st.caption("🚀 Powered by Gemini")
    # if st.button("Create New User ID"):
    #     new_user_message = "Hi there!"
    #     st.session_state.messages.append({"role": "user", "content": new_user_message})
    #     response = create_new_conversation(new_user_message, new_user_id, working_base_url)
    #     st.session_state.messages.append({"role": "assistant", "content": response})
    #     st.rerun()

st.title("AI Chatbot")
st.caption("🚀 Powered by Gemini")

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

# while True:
#     url = "https://ai-chatbot-locf.onrender.com/"
#     resp = requests.get(url)
#     print("===============================")
#     print(resp)
#     print("===============================")
#     time.sleep(10)
