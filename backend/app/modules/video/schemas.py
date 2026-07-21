from pydantic import BaseModel
from typing import List, Optional

class VideoMetadata(BaseModel):
    job_id: str
    filename: str
    fps: float
    duration: float
    total_frames: int
    width: int
    height: int
    codec: str = "unknown"
    file_size: int

class FrameMetadata(BaseModel):
    frame_id: int
    scene_id: Optional[int]
    timestamp: str
    frame_number: int
    path: str

class VideoProcessingResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict
