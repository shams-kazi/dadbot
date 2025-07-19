# july 10 2025
import streamlit as st
import os
from google import genai
from google.genai import types

# Set your Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Please set the GOOGLE_API_KEY environment variable")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=api_key)

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
            text="You are a funny chatbot  for my kids rizwan, hashim and noora pretending to be me. it is designed to encourage them to explore the world, and tell them to not play video games or use screen time "
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
        accumulated_text += chunk.text # Accumulate the text from each chunk
        # Attempt to parse the accumulated text as JSON
        chunk_json = json.loads(accumulated_text)
        response_text = chunk_json.get("response", "") # Use .get for safe access
        print(response_text, end="", flush=True)
        full_response_text += response_text
        accumulated_text = "" # Reset accumulated text on successful parse

        # response_text += response_text # TODO: fix this - to remove the response and {}
        response_area.markdown(full_response_text)

    # Append model response to history
    st.session_state.chat_history.append(
        types.Content(role="model", parts=[types.Part.from_text(text=full_response_text)])
    )

