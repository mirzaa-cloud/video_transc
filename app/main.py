import logging
import subprocess
import time
from pathlib import Path

from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException

from app.audio_extractor import extract_audio
from app.transcribe import transcribe_audio
from app.file_utils import save_json
from app.file_utils import save_text
from app.config import AUDIO_DIR, TRANSCRIPT_DIR, UPLOAD_DIR
from app.models import TranscriptionResponse

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Interview Transcription API"
)

for directory in (UPLOAD_DIR, AUDIO_DIR, TRANSCRIPT_DIR):
    directory.mkdir(parents=True, exist_ok=True)


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_video(
        file: UploadFile = File(...)
):

    request_started = time.perf_counter()

    if not file.filename:
        raise HTTPException(status_code=400, detail="A video file is required")

    logger.info("Transcription request received: filename=%s", file.filename)

    upload_path = Path(
        UPLOAD_DIR
    ) / Path(file.filename).name

    with open(upload_path, "wb") as f:

        f.write(
            await file.read()
        )

    logger.info(
        "Video uploaded successfully: path=%s size_bytes=%d",
        upload_path,
        upload_path.stat().st_size
    )

    try:
        logger.info("Voice extraction started: video=%s", upload_path)
        audio_path = extract_audio(str(upload_path))
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        logger.exception("Audio extraction failed: path=%s", upload_path)
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    logger.info("Voice extracted successfully: audio=%s", audio_path)

    logger.info("Transcription started: audio=%s", audio_path)
    transcript = transcribe_audio(
        audio_path
    )
    logger.info("Transcription completed successfully: segments=%d", len(transcript))

    transcript_json = (
        TRANSCRIPT_DIR /
        f"{upload_path.stem}.json"
    )

    transcript_txt = (
        TRANSCRIPT_DIR /
        f"{upload_path.stem}.txt"
    )

    save_json(
        transcript,
        transcript_json
    )

    save_text(
        transcript,
        transcript_txt
    )

    logger.info(
        "Transcription finished: json=%s text=%s elapsed_seconds=%.2f",
        transcript_json,
        transcript_txt,
        time.perf_counter() - request_started
    )

    return {
        "status": "success",
        "json_file": str(transcript_json),
        "text_file": str(transcript_txt)
    }