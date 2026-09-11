import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import hf_hub_download


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN is missing from the project-root .env file")

try:
    downloaded_file = hf_hub_download(
        repo_id="gpt2",
        filename="config.json",
        token=HF_TOKEN,
    )
except Exception as exc:
    print(f"Hugging Face download failed: {type(exc).__name__}: {exc}")
    raise SystemExit(1) from exc

print("Hugging Face connection and token test passed")
print(f"Downloaded file: {downloaded_file}")
