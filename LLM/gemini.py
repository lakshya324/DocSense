# Using Google Gemini LLM model
# Using Through API

import google.generativeai as genai
from run import api_key


# Load environment variables from .env file




# Configure the API
genai.configure(api_key=api_key)


def gemini(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.0-pro-latest")
    response = model.generate_content(prompt)
    return response.text
