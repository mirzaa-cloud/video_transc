import logging
import subprocess
from pathlib import Path
from shutil import which

from app.config import AUDIO_DIR, FFMPEG_PATH

logger = logging.getLogger(__name__)


def get_ffmpeg_executable():

    if FFMPEG_PATH != "ffmpeg":
        configured_path = Path(FFMPEG_PATH)
        if configured_path.is_file():
            return str(configured_path)

        resolved_path = which(FFMPEG_PATH)
        if resolved_path:
            return resolved_path

    try:
        from imageio_ffmpeg import get_ffmpeg_exe

        return get_ffmpeg_exe()
    except (ImportError, RuntimeError):
        resolved_path = which(FFMPEG_PATH)
        if resolved_path:
            return resolved_path

    raise FileNotFoundError(
        "FFmpeg was not found. Install imageio-ffmpeg or set "
        "FFMPEG_PATH in .env."
    )


def extract_audio(video_path, output_folder=AUDIO_DIR):

    ffmpeg = get_ffmpeg_executable()

    video = Path(video_path)

    audio_file = Path(output_folder) / f"{video.stem}.wav"

    command = [
        ffmpeg,
        "-i",
        str(video_path),
        "-ar",
        "16000",
        "-ac",
        "1",
        str(audio_file),
        "-y"
    ]

    logger.info("Running FFmpeg: executable=%s input=%s output=%s", ffmpeg, video_path, audio_file)
    subprocess.run(command, check=True)
    logger.info("FFmpeg complete: output=%s size_bytes=%d", audio_file, audio_file.stat().st_size)

    return str(audio_file)