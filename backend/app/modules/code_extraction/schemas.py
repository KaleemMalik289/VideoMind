from pydantic import BaseModel, Field
from typing import List, Optional

class CodeSnippet(BaseModel):
    filename: str
    timeline: str
    code: str

class CodeJSON(BaseModel):
    language: str
    confidence: float
    description: str
    files: List[CodeSnippet]

class CodeMetadata(BaseModel):
    job_id: str
    num_chunks_processed: int
    num_files_extracted: int
    syntax_valid: bool
    model_used: str
    total_tokens: int
    processing_duration_sec: float

class CodeResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict
