# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from transcription_system import ProfessionalTranscriber
# import shutil
# import os
# from pathlib import Path

# app = FastAPI()
# transcriber = ProfessionalTranscriber()

# DATA_DIR = Path("data")
# AUDIO_DIR = DATA_DIR / "audio"
# TRANSCRIPT_DIR = DATA_DIR / "transcripts"
# AUDIO_DIR.mkdir(parents=True, exist_ok=True)
# TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

# @app.post("/transcribe/")
# async def transcribe(file: UploadFile = File(...)):
#     # Save uploaded file
#     file_location = AUDIO_DIR / file.filename
#     with open(file_location, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
    
#     # Run transcription
#     result = transcriber.transcribe_audio(str(file_location))
#     srt_path = TRANSCRIPT_DIR / f"{file_location.stem}.srt"
#     transcriber.generate_srt(result, str(srt_path))

#     # Return relevant data
#     return {
#         "audio_path": str(file_location),
#         "srt_path": str(srt_path),
#         "full_text": result['full_text'],
#         "language": result['language'],
#         "probability": result['language_probability'],
#         "transcription_time": result['transcription_time']
#     }


from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import JSONResponse, FileResponse
from transcription_system import ProfessionalTranscriber
import shutil
from pathlib import Path
import os

app = FastAPI()
transcriber = ProfessionalTranscriber()

DATA_DIR = Path("data")
AUDIO_DIR = DATA_DIR / "audio"
TRANSCRIPT_DIR = DATA_DIR / "transcripts"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    # Save uploaded file
    file_location = AUDIO_DIR / file.filename
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Run transcription
    result = transcriber.transcribe_audio(str(file_location))
    srt_path = TRANSCRIPT_DIR / f"{file_location.stem}.srt"
    transcriber.generate_srt(result, str(srt_path))

    # Return relevant data (return only the filename for SRT, not the path)
    return {
        "audio_path": str(file_location),
        "srt_path": str(srt_path),
        "srt_filename": srt_path.name,   # for remote download!
        "full_text": result['full_text'],
        "language": result['language'],
        "probability": result['language_probability'],
        "transcription_time": result['transcription_time']
    }

@app.get("/download/srt/")
async def download_srt(filename: str = Query(...)):
    file_path = TRANSCRIPT_DIR / filename
    if not file_path.exists():
        return JSONResponse({"error": "File not found"}, status_code=404)
    return FileResponse(
        path=file_path,
        media_type="text/plain",
        filename=filename
    )
