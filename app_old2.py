import streamlit as st
import os
from pathlib import Path
import json
import requests
import urllib.parse

# Paths
DATA_DIR = Path("data")
AUDIO_DIR = DATA_DIR / "audio"
TRANSCRIPT_DIR = DATA_DIR / "transcripts"
SUMMARY_PATH = DATA_DIR / "summary.json"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_PATH.touch(exist_ok=True)

# Load summary
try:
    with open(SUMMARY_PATH, 'r') as f:
        summary_data = json.load(f)
except Exception:
    summary_data = {}

# ---- Sidebar Upload Panel ----
st.sidebar.title("🎙️ Upload Audio/Video")
uploaded_file = st.sidebar.file_uploader("Upload your file", type=["mp3", "wav", "mp4", "m4a"])

if uploaded_file:
    file_path = AUDIO_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.sidebar.success(f"Uploaded: {uploaded_file.name}")

    with st.spinner("Transcribing via API..."):
        api_url = "http://localhost:8000/transcribe/"  # Update if on another host/port!
        with open(file_path, "rb") as audio_file:
            files = {"file": (file_path.name, audio_file, "audio/mpeg")}
            response = requests.post(api_url, files=files)
        if response.status_code == 200:
            result = response.json()
            srt_path = result["srt_path"]
            summary_data[file_path.name] = {
                "audio_path": result["audio_path"],
                "srt_path": srt_path,
                "full_text": result["full_text"],
                "language": result["language"],
                "probability": result["probability"],
                "transcription_time": result["transcription_time"]
            }
            with open(SUMMARY_PATH, 'w') as f:
                json.dump(summary_data, f, indent=2)
            st.sidebar.success("✅ Transcription complete!")
        else:
            st.sidebar.error("Transcription failed! Check API server logs.")

# ---- Routing: Main Grid View vs Detail View ----
query_params = st.query_params
selected_file = query_params.get("file", None)

if selected_file:
    # ---- Detail View ----
    st.title(f"📄 Transcript: {selected_file}")
    data = summary_data.get(selected_file)
    if not data:
        st.error("File not found.")
    else:
        st.subheader("📝 Full Transcript")
        st.write(data["full_text"])

        col1, col2 = st.columns(2)
        with col1:
            # Show download if file exists
            if os.path.exists(data["srt_path"]):
                with open(data["srt_path"], "rb") as f:
                    st.download_button("📥 Download SRT", f, file_name=Path(data["srt_path"]).name, mime="text/plain")
        with col2:
            # You can add "regenerate" using the API as needed
            st.info("Regeneration via API not implemented in this demo.")

else:
    # ---- Main Grid View ----
    st.title("🗂️ Transcribed Files")

    if not summary_data:
        st.info("No transcriptions yet. Upload a file to get started!")
    else:
        # Show files in a responsive grid
        col_count = 5
        keys = list(summary_data.keys())
        rows = [keys[i:i+col_count] for i in range(0, len(keys), col_count)]

        for row in rows:
            cols = st.columns(len(row))
            for i, filename in enumerate(row):
                with cols[i]:
                    st.markdown(
                        f"""
                        <div style="border:1px solid #ddd; border-radius:12px; padding:10px; text-align:center; height:100px; display:flex; align-items:center; justify-content:center;">
                            <a href="/?file={urllib.parse.quote(filename)}" target="_blank" style="text-decoration:none; color:inherit;">
                                <strong>{filename}</strong>
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
