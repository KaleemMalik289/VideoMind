import os
import shutil
from pathlib import Path
from app.core.settings import settings
from loguru import logger

class StorageService:
    """Handles all file-system operations strictly within job-specific folders."""
    
    def __init__(self):
        self.base_dir = Path(settings.STORAGE_DIR)
        self.processed_dir = Path(settings.PROCESSED_DIR)
        self._ensure_base_dirs()
        
    def _ensure_base_dirs(self):
        """Creates top-level storage directories if they do not exist."""
        for d in [settings.UPLOADS_DIR, settings.PROCESSED_DIR, settings.OUTPUTS_DIR, settings.TEMP_DIR, settings.MODELS_DIR, f"{settings.STORAGE_DIR}/logs"]:
            Path(d).mkdir(parents=True, exist_ok=True)
            
    def create_job_directory(self, job_id: str) -> Path:
        """Creates the internal folder structure for a specific job."""
        job_path = self.processed_dir / job_id
        
        subdirs = [
            "original_video",
            "frames",
            "unique_frames",
            "preprocessed_frames",
            "audio",
            "transcript",
            "ocr",
            "timeline",
            "chunks",
            "summary",
            "notes",
            "code",
            "flashcards",
            "quiz",
            "exports"
        ]
        
        for subdir in subdirs:
            (job_path / subdir).mkdir(parents=True, exist_ok=True)
            
        logger.info(f"Created directory structure for job_id: {job_id}")
        return job_path
        
    def get_job_path(self, job_id: str) -> Path:
        """Returns the base path for a job, ensuring it exists."""
        job_path = self.processed_dir / job_id
        if not job_path.exists():
            raise FileNotFoundError(f"Job directory {job_id} not found.")
        return job_path

app_storage = StorageService()
