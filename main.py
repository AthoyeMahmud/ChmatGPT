import streamlit as st
from groq import Groq
import json
import time
from datetime import datetime
import os

# Muh Secrets 
api_key = st.secrets["api_keys"]["my_api_key"]
st.write("API Key:", api_key)

# Initialize Groq
client = Groq(api_key=API_KEY)

# Initialize Session State
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_settings' not in st.session_state:
    st.session_state.user_settings = {"temperature": 0.7, "max_tokens": 1000}

# Main Chat Application
def chat_interface():
    st.title("ChatGPT Clone with GroqCloud API")
    display_settings()
    display_chat()
    user_input = st.text_input("Enter your message:", key="user_input")

    if st.button("Send") and user_input:
        add_message(user_input, "user")
        with st.spinner("ChmatGPT is typing..."):  # Typing indicator
            response = query_groqcloud_api(user_input)
            time.sleep(1)  # Simulated delay
            if response:
                add_message(response, "bot")

# Display Settings
def display_settings():
    with st.sidebar:
        st.header("Settings")
        st.session_state.user_settings['temperature'] = st.slider("Temperature", 0.0, 1.0, 0.7)
        st.session_state.user_settings['max_tokens'] = st.slider("Max Tokens", 100, 500, 1000)
        st.write("Customize the AI's response behavior.")

# Display Chat Messages
def display_chat():
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.write(f"**You:** {message['content']}")
        else:
            st.write(f"**ChmatGPT:** {message['content']}")

# Add Message to Chat History
def add_message(content, role):
    st.session_state.chat_history.append({"role": role, "content": content})

# Query GroqCloud API using Groq client
def query_groqcloud_api(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3.2-90b-8192",
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Save Chat History
def save_chat():
    filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as file:
        json.dump(st.session_state.chat_history, file)
    st.success(f"Chat history saved as {filename}")

# Load Chat History
def load_chat():
    uploaded_file = st.file_uploader("Load Chat History", type="json")
    if uploaded_file:
        st.session_state.chat_history = json.load(uploaded_file)
        st.success("Chat history loaded successfully")

# App Structure
chat_interface()
if st.button("Save Chat History"):
    save_chat()
load_chat()
