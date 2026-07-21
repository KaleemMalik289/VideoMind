from pydantic import BaseModel
from typing import List

class PreprocessingMetadata(BaseModel):
    frame_id: int
    original_image: str
    processed_image: str
    operations: List[str]

class PreprocessingResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict
