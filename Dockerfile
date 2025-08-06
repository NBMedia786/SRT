
FROM nvidia/cuda:12.9.1-cudnn-devel-ubuntu22.04


WORKDIR /app


RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1


COPY ./api_server.py .
COPY ./transcription_system.py .


RUN pip install --no-cache-dir \
    torch \
    torchaudio \
    torchvision\
    --index-url https://download.pytorch.org/whl/cu121 && \
    pip install --no-cache-dir \
    librosa \
    scipy \
    webrtcvad-wheels \
    soundfile \
    faster-whisper \
    streamlit


# Expose FastAPI default port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0","--server.enableCORS=false","--server.enableXsrfProtection=false"]



