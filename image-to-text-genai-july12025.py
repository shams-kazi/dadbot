import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64

load_dotenv()



# --- Configure Gemini API ---
#GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
#if not GOOGLE_API_KEY:
#    st.error("GOOGLE_API_KEY environment variable not set.")
#    st.stop()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Image Loader Function ---
def load_image(image_file=None, image_url=None):
    try:
        if image_url:
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        elif image_file:
            image = Image.open(image_file)
        else:
            return None
        return image
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# --- Gemini API Interaction ---
def get_image_description(image: Image.Image) -> str:
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(image)
        return response.text
    except Exception as e:
        return f"An error occurred while getting the image description: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="Image Description Chatbot")
st.title("🖼️ Image Description using Gemini API")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
image_url = st.text_input("Or enter an image URL")

if st.button("Get Description"):
    image = load_image(image_file=uploaded_file, image_url=image_url)

    if image:
        st.image(image, caption="Input Image", use_column_width=True)
        with st.spinner("Generating description..."):
            description = get_image_description(image)
        st.subheader("📄 Description:")
        st.write(description)
    else:
        st.warning("Please upload a valid image or provide a valid image URL.")
