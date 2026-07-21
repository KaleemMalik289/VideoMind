from pydantic import BaseModel
from typing import List

class SemanticChunk(BaseModel):
    chunk_id: int
    start: float
    end: float
    transcript: str
    ocr_text: List[str]
    frames: List[int]
    estimated_tokens: int

class ChunkJSON(BaseModel):
    job_id: str
    chunks: List[SemanticChunk]

class ChunkMetadata(BaseModel):
    job_id: str
    num_chunks: int
    avg_chunk_size_sec: float
    avg_token_count: float
    processing_duration_sec: float
    
class ChunkResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict
