import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile
from app.services.storage_service import app_storage
from loguru import logger
from app.core.exceptions import BaseAPIException

class UploadService:
    """Coordinates the uploading and initial processing pipeline triggers."""
    
    @staticmethod
    async def process_upload(file: UploadFile) -> str:
        """Saves an uploaded file and initializes a processing job."""
        
        # 1. Validate file (basic check)
        if not file.content_type.startswith("video/"):
            raise BaseAPIException("Invalid file type. Only videos are supported.", "INVALID_FILE_TYPE", status_code=400)
            
        # 2. Generate Job ID
        job_id = str(uuid.uuid4())
        logger.info(f"Starting upload process for job_id: {job_id}")
        
        # 3. Create job directory structure
        job_path = app_storage.create_job_directory(job_id)
        
        # 4. Save original video
        video_dir = job_path / "original_video"
        file_path = video_dir / file.filename
        
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logger.info(f"Saved video file for job_id: {job_id} to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save video for job_id: {job_id}: {str(e)}")
            raise BaseAPIException("Failed to save uploaded file.", "UPLOAD_FAILED", status_code=500)
            
        # 5. TODO: Trigger Background Processing (Celery task) here
        
        return job_id
