from pydantic import BaseModel
from typing import List

class SummaryJSON(BaseModel):
    executive_summary: str
    detailed_summary: str
    bullet_summary: List[str]

class SummaryMetadata(BaseModel):
    job_id: str
    num_chunks_processed: int
    model_used: str
    total_tokens: int
    processing_duration_sec: float

class SummaryResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict
