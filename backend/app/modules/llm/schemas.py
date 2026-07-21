from pydantic import BaseModel
from typing import List, Optional

class LLMChunkResponse(BaseModel):
    chunk_id: int
    start: float
    end: float
    content: str
    tokens_used: int = 0
    model: str = ""

class LLMJobResponse(BaseModel):
    job_id: str
    responses: List[LLMChunkResponse]

class LLMMetadata(BaseModel):
    job_id: str
    provider: str
    model: str
    total_tokens: int
    processing_duration_sec: float
    num_chunks: int

class FinalResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict
