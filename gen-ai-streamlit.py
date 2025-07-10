# july 10 2025
import streamlit as st
from google import genai
from google.genai import types

# Set your Gemini API key

# Initialize Gemini client
client = genai.Client()

# Configure response
generate_content_config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "response": genai.types.Schema(type=genai.types.Type.STRING),
        },
    ),
    system_instruction=[
        types.Part.from_text(
            text="You are a chatbot that helps students clarify their doubts in a simple way."
        ),
    ],
)

model = "gemini-2.0-flash"

# Streamlit UI setup
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("📚 Dad Kazi in a bot")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text input
user_input = st.chat_input("Ask a question...")

# When user sends a message
if user_input:
    # Append user message to history
    st.session_state.chat_history.append(
        types.Content(role="user", parts=[types.Part.from_text(text=user_input)])
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Stream response
    response_text = ""
    with st.chat_message("assistant"):
        response_area = st.empty()
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=st.session_state.chat_history,
            config=generate_content_config,
        ):
            response_text += chunk.text # TODO: fix this - to remove the response and {}
            response_area.markdown(response_text)

    # Append model response to history
    st.session_state.chat_history.append(
        types.Content(role="model", parts=[types.Part.from_text(text=response_text)])
    )

