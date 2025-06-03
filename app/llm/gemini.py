import os
from typing import Optional

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini 2.0 Flash
GEMINI_MODEL = "models/gemini-1.5-flash"
API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY is not set in the environment")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)


def run_gemini(prompt: str) -> str:
    """Run a prompt through the Gemini model and return the response.
    
    Args:
        prompt: The prompt to send to the model
        
    Returns:
        The model's response as a string
        
    Raises:
        RuntimeError: If there's an error generating the response
    """
    try:
        response = model.generate_content(prompt)
        # Handle different response types
        if hasattr(response, 'text') and callable(response.text):
            return response.text().strip()
        elif hasattr(response, 'text') and response.text is not None:
            return str(response.text).strip()
        else:
            return str(response).strip()
    except Exception as e:
        raise RuntimeError(f"Error generating response from Gemini: {str(e)}")
