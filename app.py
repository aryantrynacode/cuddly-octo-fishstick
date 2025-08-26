import streamlit as st
import os
from utils.transcription import transcribe_audio
from utils.summarization import summarize_text
from utils.qna import ask_question
from google import genai


# -------------------- Load API Key --------------------

api_key = st.secrets.get("GOOGLE_API_KEY")  # safer using .get()
if not api_key:
    st.error("Google API key not found. Please set GOOGLE_API_KEY in Streamlit secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# -------------------- Page Setup --------------------
st.set_page_config(
    page_title="🎙️ Audio Transcription + QnA ",
    layout="wide"
)
st.title("🎙️ Upload or Record Audio → Transcription, Summarization & QnA ")

# -------------------- Session State --------------------
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "file_path" not in st.session_state:
    st.session_state.file_path = None

# -------------------- Audio Save Function --------------------
def save_audio(file_content, filename):
    """
    Saves audio to disk.
    If file_content is an UploadedFile, it reads bytes automatically.
    If file_content is already bytes, it writes directly.
    """
    import streamlit as st

    # Check if the object is UploadedFile
    if hasattr(file_content, "read"):
        file_content = file_content.read()  # Convert UploadedFile to bytes

    # Write bytes to file
    with open(filename, "wb") as f:
        f.write(file_content)
    return filename


# -------------------- Tabs --------------------
tab1, tab2, tab3 = st.tabs(["🎧 Audio", "📝 Summary", "❓ QnA"])

# -------------------- Tab 1: Audio Upload / Recording --------------------
with tab1:
    st.subheader("Upload or Record Audio")

    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])
    recorded_file = st.audio_input("Or record directly")  # returns bytes

    if uploaded_file:
        st.session_state.file_path = save_audio(uploaded_file, uploaded_file.name)
        st.audio(st.session_state.file_path)
    elif recorded_file:
        st.session_state.file_path = save_audio(recorded_file, "recorded_audio.wav")
        st.audio(st.session_state.file_path)

    if st.session_state.file_path:
        if st.button("Transcribe Audio"):
            with st.spinner("Transcribing..."):
                st.session_state.transcript = transcribe_audio(st.session_state.file_path)
            st.success("✅ Transcription completed!")
            st.subheader("📝 Transcript")
            st.write(st.session_state.transcript)

# -------------------- Tab 2: Summarization --------------------
with tab2:
    st.subheader("Summarize Transcript")
    if st.session_state.transcript:
        if st.button("Generate Summary"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(st.session_state.transcript)
            st.subheader("📌 Summary")
            st.write(summary)
    else:
        st.info("Please transcribe audio first in the Audio tab.")

# -------------------- Tab 3: QnA --------------------
with tab3:
    st.subheader("Ask Questions About Transcript")
    if st.session_state.transcript:
        question = st.text_input("Enter your question here:")
        if question and st.button("Get Answer"):
            with st.spinner("Generating answer..."):
                answer = ask_question(st.session_state.transcript, question)
            st.subheader("💡 Answer")
            st.write(answer)
    else:
        st.info("Please transcribe audio first in the Audio tab.")





