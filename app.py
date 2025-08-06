

# import streamlit as st
# import os
# from pathlib import Path
# import json
# import requests
# import urllib.parse

# # --- CONFIG: Set this to your backend server's IP!
# API_HOST = "http://192.168.0.107:8000/"  # <-- Change this to your backend/model PC's IP address

# DATA_DIR = Path("data")
# AUDIO_DIR = DATA_DIR / "audio"
# SUMMARY_PATH = DATA_DIR / "summary.json"

# AUDIO_DIR.mkdir(parents=True, exist_ok=True)
# SUMMARY_PATH.touch(exist_ok=True)

# # --- Load summary data ---
# try:
#     with open(SUMMARY_PATH, 'r') as f:
#         summary_data = json.load(f)
# except Exception:
#     summary_data = {}

# # --- Upload Panel (Multi-upload) ---
# st.sidebar.title("🎙️ Upload Audio/Video")
# uploaded_files = st.sidebar.file_uploader(
#     "Upload files", type=["mp3", "wav", "mp4", "m4a"], accept_multiple_files=True
# )

# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         file_path = AUDIO_DIR / uploaded_file.name
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.read())
#         st.sidebar.success(f"Uploaded: {uploaded_file.name}")

#         with st.spinner(f"Transcribing {uploaded_file.name} via API..."):
#             api_url = f"{API_HOST}/transcribe/"
#             with open(file_path, "rb") as audio_file:
#                 files = {"file": (file_path.name, audio_file, "audio/mpeg")}
#                 response = requests.post(api_url, files=files)
#             if response.status_code == 200:
#                 result = response.json()
#                 # Store the filename for remote download
#                 summary_data[file_path.name] = {
#                     "audio_path": result["audio_path"],
#                     "srt_path": result["srt_path"],        # still show path for info
#                     "srt_filename": result["srt_filename"], # for download endpoint
#                     "full_text": result["full_text"],
#                     "language": result["language"],
#                     "probability": result["probability"],
#                     "transcription_time": result["transcription_time"]
#                 }
#                 with open(SUMMARY_PATH, 'w') as f:
#                     json.dump(summary_data, f, indent=2)
#                 st.sidebar.success(f"✅ Transcription complete: {uploaded_file.name}")
#             else:
#                 st.sidebar.error(f"Transcription failed for {uploaded_file.name}!")

# # --- Routing: Main Grid View vs Detail View ---
# query_params = st.query_params
# selected_file = query_params.get("file", None)

# if selected_file:
#     # --- Detail View ---
#     st.title(f"📄 Transcript: {selected_file}")
#     data = summary_data.get(selected_file)
#     if not data:
#         st.error("File not found.")
#     else:
#         st.subheader("📝 Full Transcript")
#         st.write(data["full_text"])

#         col1, col2 = st.columns(2)
#         with col1:
            
#             srt_filename = data.get("srt_filename")
#             if srt_filename:
                
#                 api_host = API_HOST.rstrip("/")
#                 srt_url = f"{api_host}/download/srt/?filename={urllib.parse.quote(srt_filename)}"
#                 custom_btn = f"""
#                 <a href="{srt_url}" download="{srt_filename}" style="
#                     display: inline-block;
#                     padding: 0.5em 1.2em;
#                     border-radius: 6px;
#                     background: #00B050;
#                     color: white;
#                     font-weight: 600;
#                     text-decoration: none;
#                     font-size: 1.07em;
#                     margin-top: 0.5em;
#                     box-shadow: 0 2px 8px rgba(0,0,0,0.03);
#                     transition: background 0.2s;
#                     cursor: pointer;
#                 " onmouseover="this.style.background='#009040'" onmouseout="this.style.background='#00B050'">
#                     📥 Download SRT
#                 </a>
#                 """
#                 st.markdown(custom_btn, unsafe_allow_html=True)
#             else:
#                 st.warning("No SRT available for download. Try regenerating.")


#         # with col2:
#         #     if st.button("♻️ Regenerate Transcript"):
#         #         with st.spinner("Re-transcribing via API..."):
#         #             api_url = f"{API_HOST}/transcribe/"
#         #             audio_path = data["audio_path"]
#         #             with open(audio_path, "rb") as audio_file:
#         #                 files = {"file": (Path(audio_path).name, audio_file, "audio/mpeg")}
#         #                 response = requests.post(api_url, files=files)
#         #             if response.status_code == 200:
#         #                 result = response.json()
#         #                 summary_data[selected_file] = {
#         #                     "audio_path": result["audio_path"],
#         #                     "srt_path": result["srt_path"],
#         #                     "srt_filename": result["srt_filename"],
#         #                     "full_text": result["full_text"],
#         #                     "language": result["language"],
#         #                     "probability": result["probability"],
#         #                     "transcription_time": result["transcription_time"]
#         #                 }
#         #                 with open(SUMMARY_PATH, 'w') as f:
#         #                     json.dump(summary_data, f, indent=2)
#         #                 st.success("🔁 Transcript regenerated!")
#         #                 st.rerun()
#         #             else:
#         #                 st.error("Failed to regenerate transcript. Check API server.")
#         with col2:
#             srt_filename = data.get("srt_filename")
#             file_name_encoded = urllib.parse.quote(selected_file)
#             # This submits the form by reloading the page with ?file=...&regenerate=1
#             regenerate_btn_html = f"""
#             <form action="/?file={file_name_encoded}&regenerate=1" method="get">
#                 <input type="hidden" name="file" value="{selected_file}">
#                 <input type="hidden" name="regenerate" value="1">
#                 <button type="submit" style="
#                     display: inline-block;
#                     padding: 0.5em 1.2em;
#                     border-radius: 6px;
#                     background: #00B050;
#                     color: white;
#                     font-weight: 600;
#                     font-size: 1.07em;
#                     margin-top: 0.5em;
#                     border: none;
#                     box-shadow: 0 2px 8px rgba(0,0,0,0.03);
#                     cursor: pointer;
#                     transition: background 0.2s;
#                 " onmouseover="this.style.background='#009040'" onmouseout="this.style.background='#00B050'">
#                     ♻️ Regenerate Transcript
#                 </button>
#             </form>
#             """
#             st.markdown(regenerate_btn_html, unsafe_allow_html=True)

# else:
#     # --- Main Grid View ---
#     st.title("🗂️ Transcribed Files")

#     if not summary_data:
#         st.info("No transcriptions yet. Upload a file to get started!")
#     else:
#         col_count = 5
#         keys = list(summary_data.keys())
#         rows = [keys[i:i+col_count] for i in range(0, len(keys), col_count)]

#         for row in rows:
#             cols = st.columns(len(row))
#             for i, filename in enumerate(row):
#                 with cols[i]:
#                     st.markdown(
#                         f"""
#                         <div style="border:1px solid #ddd; border-radius:12px; padding:10px; text-align:center; height:100px; display:flex; align-items:center; justify-content:center;">
#                             <a href="/?file={urllib.parse.quote(filename)}" target="_blank" style="text-decoration:none; color:inherit;">
#                                 <strong>{filename}</strong>
#                             </a>
#                         </div>
#                         """,
#                         unsafe_allow_html=True
#                     )















import streamlit as st
import os
from pathlib import Path
import json
import requests
import urllib.parse

# --- CONFIG: Set this to your backend server's IP!
API_HOST = "http://192.168.0.107:8000"  # <-- Change this to your backend/model PC's IP address

DATA_DIR = Path("data")
AUDIO_DIR = DATA_DIR / "audio"
SUMMARY_PATH = DATA_DIR / "summary.json"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_PATH.touch(exist_ok=True)

# --- Load summary data ---
try:
    with open(SUMMARY_PATH, 'r') as f:
        summary_data = json.load(f)
except Exception:
    summary_data = {}

# --- Upload Panel (Multi-upload) ---
st.sidebar.title("🎙️ Upload Audio/Video")
uploaded_files = st.sidebar.file_uploader(
    "Upload files", type=["mp3", "wav", "mp4", "m4a"], accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = AUDIO_DIR / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        st.sidebar.success(f"Uploaded: {uploaded_file.name}")

        with st.spinner(f"Transcribing {uploaded_file.name} via API..."):
            api_url = f"{API_HOST.rstrip('/')}/transcribe/"
            with open(file_path, "rb") as audio_file:
                files = {"file": (file_path.name, audio_file, "audio/mpeg")}
                response = requests.post(api_url, files=files)
            if response.status_code == 200:
                result = response.json()
                summary_data[file_path.name] = {
                    "audio_path": result["audio_path"],
                    "srt_path": result["srt_path"],
                    "srt_filename": result["srt_filename"],
                    "full_text": result["full_text"],
                    "language": result["language"],
                    "probability": result["probability"],
                    "transcription_time": result["transcription_time"]
                }
                with open(SUMMARY_PATH, 'w') as f:
                    json.dump(summary_data, f, indent=2)
                st.sidebar.success(f"✅ Transcription complete: {uploaded_file.name}")
            else:
                st.sidebar.error(f"Transcription failed for {uploaded_file.name}!")

# --- Routing: Main Grid View vs Detail View ---
query_params = st.query_params
selected_file = query_params.get("file", None)
regenerate = query_params.get("regenerate", None)

# --- Regenerate Transcript Handler ---
if selected_file and regenerate == "1":
    data = summary_data.get(selected_file)
    if data:
        with st.spinner("Re-transcribing via API..."):
            api_url = f"{API_HOST.rstrip('/')}/transcribe/"
            audio_path = data["audio_path"]
            with open(audio_path, "rb") as audio_file:
                files = {"file": (Path(audio_path).name, audio_file, "audio/mpeg")}
                response = requests.post(api_url, files=files)
            if response.status_code == 200:
                result = response.json()
                summary_data[selected_file] = {
                    "audio_path": result["audio_path"],
                    "srt_path": result["srt_path"],
                    "srt_filename": result["srt_filename"],
                    "full_text": result["full_text"],
                    "language": result["language"],
                    "probability": result["probability"],
                    "transcription_time": result["transcription_time"]
                }
                with open(SUMMARY_PATH, 'w') as f:
                    json.dump(summary_data, f, indent=2)
                st.success("🔁 Transcript regenerated!")
                # Remove ?regenerate=1 from URL to prevent looping
                st.query_params["file"] = selected_file
                if "regenerate" in st.query_params:
                    del st.query_params["regenerate"]
                st.stop()
            else:
                st.error("Failed to regenerate transcript. Check API server.")
                st.stop()

if selected_file:
    # --- Detail View ---
    st.title(f"📄 Transcript: {selected_file}")
    data = summary_data.get(selected_file)
    if not data:
        st.error("File not found.")
    else:
        st.subheader("📝 Full Transcript")
        st.write(data["full_text"])

        col1, col2 = st.columns(2)
        with col1:
            srt_filename = data.get("srt_filename")
            if srt_filename:
                api_host = API_HOST.rstrip("/")
                srt_url = f"{api_host}/download/srt/?filename={urllib.parse.quote(srt_filename)}"
                custom_btn = f"""
                <a href="{srt_url}" download="{srt_filename}" style="
                    display: inline-block;
                    padding: 0.5em 1.2em;
                    border-radius: 6px;
                    background: #00B050;
                    color: white;
                    font-weight: 600;
                    font-size: 1.07em;
                    margin-top: 1em;
                    border: none;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
                    cursor: pointer;
                    transition: background 0.2s;
                    text-decoration: none;  /* Ensure no underline */
                " onmouseover="this.style.background='#009040'" onmouseout="this.style.background='#00B050'">
                    📥 Download SRT
                </a>
                """
                st.markdown(custom_btn, unsafe_allow_html=True)
            else:
                st.warning("No SRT available for download. Try regenerating.")

        with col2:
            st.markdown("""
            <style>
            div.stButton > button:first-child {
                display: inline-block;
                padding: 0.5em 1.2em;
                border-radius: 6px;
                background: #00B050;
                color: white;
                font-weight: 600;
                font-size: 1.07em;
                margin-top: 0em;
                margin-left: 5em;
                border: none;
                box-shadow: 0 2px 8px rgba(0,0,0,0.03);
                cursor: pointer;
                transition: background 0.2s;
            }
            div.stButton > button:hover {
                background-color: #009040;
            }
            </style>
            """, unsafe_allow_html=True)

            regenerate_click = st.button("♻️ Regenerate Transcript", key=f"regen-{selected_file}")
            if regenerate_click:
                with st.spinner("Re-transcribing via API..."):
                    api_url = f"{API_HOST.rstrip('/')}/transcribe/"
                    audio_path = data["audio_path"]
                    with open(audio_path, "rb") as audio_file:
                        files = {"file": (Path(audio_path).name, audio_file, "audio/mpeg")}
                        response = requests.post(api_url, files=files)
                    if response.status_code == 200:
                        result = response.json()
                        summary_data[selected_file] = {
                            "audio_path": result["audio_path"],
                            "srt_path": result["srt_path"],
                            "srt_filename": result["srt_filename"],
                            "full_text": result["full_text"],
                            "language": result["language"],
                            "probability": result["probability"],
                            "transcription_time": result["transcription_time"]
                        }
                        with open(SUMMARY_PATH, 'w') as f:
                            json.dump(summary_data, f, indent=2)
                        st.success("🔁 Transcript regenerated!")
                        st.rerun()
                    else:
                        st.error("Failed to regenerate transcript. Check API server.")

else:
    # --- Main Grid View ---
    st.title("🗂️ Transcribed Files")

    if not summary_data:
        st.info("No transcriptions yet. Upload a file to get started!")
    else:
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
