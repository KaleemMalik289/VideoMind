from pydantic import BaseModel
from typing import List, Optional

class TranscriptSegment(BaseModel):
    segment_id: int
    start: float
    end: float
    text: str

class TranscriptJSON(BaseModel):
    job_id: str
    language: str
    duration: float
    segments: List[TranscriptSegment]

class TranscriptMetadata(BaseModel):
    job_id: str
    audio_duration: float
    language: str
    whisper_model: str
    processing_time_sec: float
    number_of_segments: int
    total_words: int
    
class TranscriptionResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict
