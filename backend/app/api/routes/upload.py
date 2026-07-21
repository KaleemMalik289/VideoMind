from fastapi import APIRouter, UploadFile, File
from app.schemas.upload import UploadResponse
from app.services.upload_service import UploadService

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_video(file: UploadFile = File(...)):
    """Uploads a video, generates a job ID, and triggers background processing."""
    job_id = await UploadService.process_upload(file)
    
    return UploadResponse(
        success=True,
        job_id=job_id,
        message="Video uploaded successfully. Background processing started."
    )
