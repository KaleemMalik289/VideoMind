import os
import uuid
import shutil
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile
from app.core.settings import settings
from loguru import logger
from app.modules.upload.exceptions import StorageError

class UploadStorage:
    """Handles file-system operations for the upload module."""
    
    @staticmethod
    def generate_job_id() -> str:
        """Generates a globally unique Job ID with a human-readable prefix."""
        return f"job_{uuid.uuid4().hex[:10]}"

    @staticmethod
    def create_job_directory(job_id: str) -> Path:
        """Creates the isolated folder structure for a specific job."""
        job_path = Path(settings.PROCESSED_DIR) / job_id
        
        try:
            # We create 'original' inside the job path as per specs
            original_dir = job_path / "original"
            original_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory structure for job_id: {job_id}")
            return original_dir
        except Exception as e:
            logger.error(f"Failed to create job directory for {job_id}: {str(e)}")
            raise StorageError(f"Failed to initialize storage for job {job_id}.")

    @staticmethod
    async def save_upload_file(file: UploadFile, job_id: str, sanitized_filename: str) -> Tuple[str, str, int]:
        """Saves the uploaded file to the job's original directory using asynchronous chunk streaming."""
        import aiofiles
        original_dir = UploadStorage.create_job_directory(job_id)
        file_path = original_dir / sanitized_filename
        
        try:
            # Ensure pointer is at start
            await file.seek(0)
            async with aiofiles.open(file_path, "wb") as buffer:
                while chunk := await file.read(1024 * 1024): # 1MB chunks
                    await buffer.write(chunk)
                
            file_size = os.path.getsize(file_path)
            logger.info(f"Successfully saved file {sanitized_filename} for job {job_id}.")
            
            absolute_path = str(file_path.resolve())
            relative_path = str(file_path.relative_to(Path.cwd()))
            
            return absolute_path, relative_path, file_size
        except Exception as e:
            logger.error(f"Failed to save file {sanitized_filename} for job {job_id}: {str(e)}")
            raise StorageError("Failed to write file to disk.")
