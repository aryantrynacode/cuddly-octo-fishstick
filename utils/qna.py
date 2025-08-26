from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()
os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_question(transcript: str, question: str) -> str:
    """
    Answers a question based on the transcript using Gemini.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                f"Here is a transcript:\n{transcript}\n\nQuestion: {question}\nAnswer based only on the transcript:"
            ]
        )
        return response.text
    except Exception as e:
        return f"Error in QnA (Gemini): {str(e)}"