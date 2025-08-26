from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()
os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize_text(transcript: str) -> str:
    """
    Summarizes a given transcript using Gemini.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Summarize the following text in a concise way:\n\n{transcript}"
        )
        return response.text
    except Exception as e:
        return f"Error in summarization (Gemini): {str(e)}"
