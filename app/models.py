from pydantic import BaseModel


class TranscriptionResponse(BaseModel):
    status: str
    json_file: str
    text_file: str
