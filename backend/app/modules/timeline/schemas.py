from pydantic import BaseModel
from typing import List, Optional

class TimelineEntry(BaseModel):
    timeline_id: int
    start: float
    end: float
    transcript: Optional[str] = None
    ocr_text: List[str] = []
    frame_id: Optional[int] = None
    frame_path: Optional[str] = None

class TimelineJSON(BaseModel):
    job_id: str
    entries: List[TimelineEntry]

class TimelineMetadata(BaseModel):
    job_id: str
    num_entries: int
    ocr_segments_merged: int
    transcript_segments_merged: int
    processing_duration_sec: float
    
class TimelineResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict
