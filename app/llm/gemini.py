import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini 2.0 Flash
GEMINI_MODEL = "models/gemini-1.5-flash"
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY is not set in the environment")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)


def run_gemini(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip
