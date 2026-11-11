
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key
load_dotenv()

# Page settings
st.set_page_config(
    page_title="My Personal AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 My Personal AI Assistant")
st.caption("Your own AI chatbot, built with Python")

# Check Gemini API key
# Check Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("Gemini API key not found. Please configure Streamlit Secrets.")
    st.stop()

# Connect to Gemini
client = genai.Client(api_key=api_key)

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Ask me anything...")

if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                # Convert conversation history for Gemini
                history = [
                    {
                        "role": "user" if msg["role"] == "user" else "model",
                        "parts": [{"text": msg["content"]}]
                    }
                    for msg in st.session_state.messages
                ]

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=history,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "You are a helpful personal AI assistant. "
                            "Answer in simple and clear language. "
                            "Explain difficult topics step by step."
                        )
                    )
                )

                answer = response.text
                st.markdown(answer)

                # Save AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")
