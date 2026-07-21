import re
import os
from pathlib import Path
from fastapi import UploadFile
from app.core.settings import settings
from app.modules.upload.exceptions import (
    UnsupportedFileTypeError,
    FileSizeExceededError,
    EmptyFileError,
    FilenameSanitizationError
)
from loguru import logger

class UploadValidator:
    """Validates and sanitizes file uploads."""
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitizes filename to prevent path traversal and remove special chars."""
        if not filename:
            raise FilenameSanitizationError("Filename cannot be empty.")
            
        # Basic sanitization
        safe_name = os.path.basename(filename)
        safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', safe_name)
        
        if not safe_name or safe_name == '_' or safe_name.startswith('.'):
            # Give it a default safe name if completely stripped
            safe_name = "upload_video" + Path(filename).suffix
            
        return safe_name

    @staticmethod
    async def validate_file(file: UploadFile) -> str:
        """Validates extension, MIME type, size, and sanitizes filename. Returns sanitized name."""
        
        # 1. Check if empty file object
        if not file.filename:
            raise EmptyFileError()

        # 2. Extract and validate extension
        ext = Path(file.filename).suffix.lower()
        if ext not in settings.ALLOWED_VIDEO_EXTENSIONS:
            logger.warning(f"Rejected extension: {ext}")
            raise UnsupportedFileTypeError(details={"allowed_extensions": settings.ALLOWED_VIDEO_EXTENSIONS})
            
        # 3. Validate MIME type
        if file.content_type not in settings.ALLOWED_MIME_TYPES:
            logger.warning(f"Rejected MIME type: {file.content_type}")
            raise UnsupportedFileTypeError(
                message="Invalid MIME type.", 
                details={"allowed_mime_types": settings.ALLOWED_MIME_TYPES}
            )

        # 4. Validate File Size
        # Seek to end to check size without reading entire file into memory
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0) # Reset pointer
        
        if file_size == 0:
            raise EmptyFileError()
            
        if file_size > settings.MAX_UPLOAD_SIZE:
            logger.warning(f"Rejected file size: {file_size} bytes")
            raise FileSizeExceededError(details={"max_size_bytes": settings.MAX_UPLOAD_SIZE})
            
        return UploadValidator.sanitize_filename(file.filename)
