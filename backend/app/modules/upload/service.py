from datetime import datetime, timezone
from fastapi import UploadFile
from app.modules.upload.validator import UploadValidator
from app.modules.upload.storage import UploadStorage
from app.modules.upload.schemas import UploadMetadata
from loguru import logger

class UploadService:
    """Orchestrates the local video upload pipeline."""
    
    @staticmethod
    async def process_local_upload(file: UploadFile) -> UploadMetadata:
        """Handles validation, storage, and metadata generation for a local upload."""
        logger.info(f"Starting local upload process for file: {file.filename}")
        
        # 1. Validate
        sanitized_filename = await UploadValidator.validate_file(file)
        
        # 2. Generate Job ID
        job_id = UploadStorage.generate_job_id()
        
        # 3. Store
        absolute_path, relative_path, file_size = UploadStorage.save_upload_file(
            file=file, 
            job_id=job_id, 
            sanitized_filename=sanitized_filename
        )
        
        # 4. Extract Metadata
        metadata = UploadMetadata(
            job_id=job_id,
            original_filename=file.filename,
            stored_filename=sanitized_filename,
            upload_timestamp=datetime.now(timezone.utc),
            file_size=file_size,
            file_extension=sanitized_filename.split(".")[-1] if "." in sanitized_filename else "",
            mime_type=file.content_type or "application/octet-stream",
            upload_source="local",
            absolute_storage_path=absolute_path,
            relative_storage_path=relative_path
        )
        
        logger.info(f"Completed local upload process for job {job_id}.")
        return metadata
