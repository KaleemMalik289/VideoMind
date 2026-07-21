from pydantic import BaseModel
from typing import List, Optional

class NoteSection(BaseModel):
    title: str
    content: List[str]
    definitions: Optional[List[str]] = []
    examples: Optional[List[str]] = []
    formulas: Optional[List[str]] = []

class NotesJSON(BaseModel):
    title: str
    introduction: str
    sections: List[NoteSection]
    conclusions: List[str]

class NotesMetadata(BaseModel):
    job_id: str
    num_chunks_processed: int
    model_used: str
    total_tokens: int
    processing_duration_sec: float

class NotesResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict
