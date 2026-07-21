from pydantic import BaseModel
from typing import Optional

class AudioMetadata(BaseModel):
    job_id: str
    duration: float
    sample_rate: int
    channels: int
    codec: str
    file_size: int

class AudioResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict
