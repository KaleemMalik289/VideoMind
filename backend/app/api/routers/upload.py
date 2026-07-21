from fastapi import APIRouter, UploadFile, File
from app.schemas.response import APIResponse
from app.modules.upload.service import UploadService
from loguru import logger

router = APIRouter(tags=["Upload"])

@router.post("/upload", response_model=APIResponse)
async def upload_local_video(file: UploadFile = File(...)):
    """Uploads a local video and returns the Job ID."""
    metadata = await UploadService.process_local_upload(file)
    
    # Normally, background tasks would be triggered here using BackgroundTasks
    # For now, it returns the job_id
    
    return APIResponse(
        success=True,
        message="Video uploaded successfully.",
        data={
            "job_id": metadata.job_id,
            "status": "processing",
            "filename": metadata.original_filename,
            "file_size": metadata.file_size
        }
    )
