import streamlit as st
from google import genai
from google.genai import types

api_key = st.secrets.get["GOOGLE_API_KEY"]
client = genai.Client(api_key=api_key)

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes an audio file using Gemini (Google GenAI).
    """
    try:
        # For inline small files: read bytes and send directly
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
        
        audio_part = types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/" + file_path.split('.')[-1]
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Transcribe the following audio:",
                audio_part
            ]
        )
        return response.text

    except Exception as e:
        return f"Error in transcription (Gemini): {str(e)}"