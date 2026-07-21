from pydantic import BaseModel, Field
from datetime import datetime

class UploadMetadata(BaseModel):
    job_id: str
    original_filename: str
    stored_filename: str
    upload_timestamp: datetime
    file_size: int
    file_extension: str
    mime_type: str
    upload_source: str
    absolute_storage_path: str
    relative_storage_path: str

class LocalUploadResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict

class YouTubeUploadRequest(BaseModel):
    url: str

class YouTubeUploadResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict
