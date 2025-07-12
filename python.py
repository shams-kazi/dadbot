
for i in range(5):
    print("Hello, World!")
import requests
import base64
import os
from google import genai
from google.genai import types

myname = "Shams"
r = requests.get(f"https://api.agify.io?name={myname}")
print(r.json())
print(r)

# To run this code you need to install the following dependencies:
# pip install google-genai


my_key = # gemini key

def generate():
    client = genai.Client(
        api_key= my_key, # gemini key
    )

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="what is the typical weather in kuwait in June"),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()

