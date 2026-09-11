import logging
import time

from app.config import WHISPER_MODEL, DEVICE, COMPUTE_TYPE

logger = logging.getLogger(__name__)

model = None


def get_model():
    global model

    if model is None:
        from faster_whisper import WhisperModel

        logger.info(
            "Loading Whisper model: model=%s device=%s compute_type=%s",
            WHISPER_MODEL,
            DEVICE,
            COMPUTE_TYPE
        )
        model = WhisperModel(
            WHISPER_MODEL,
            device=DEVICE,
            compute_type=COMPUTE_TYPE
        )
        logger.info("Whisper model loaded")

    return model


def transcribe_audio(audio_path):
    started = time.perf_counter()
    logger.info("Whisper transcription running: audio=%s", audio_path)
    segments, info = get_model().transcribe(
        audio_path,
        beam_size=5
    )

    transcript_data = []

    for segment in segments:
        transcript_data.append(
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            }
        )

    logger.info(
        "Whisper transcription finished: segments=%d elapsed_seconds=%.2f",
        len(transcript_data),
        time.perf_counter() - started
    )
    return transcript_data