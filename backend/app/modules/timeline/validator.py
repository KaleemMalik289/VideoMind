import os
from loguru import logger
from app.modules.timeline.exceptions import TimelineValidationError

class TimelineValidator:
    """Validates that OCR and Transcript dependencies exist before building."""
    
    @staticmethod
    def validate(ocr_dir: str, transcript_path: str) -> None:
        if not os.path.exists(transcript_path):
            logger.error(f"Missing transcript file: {transcript_path}")
            raise TimelineValidationError(details={"path": transcript_path, "reason": "Transcript JSON is missing"})
            
        if not os.path.exists(ocr_dir) or not os.path.isdir(ocr_dir):
            logger.error(f"Missing or invalid OCR directory: {ocr_dir}")
            raise TimelineValidationError(details={"path": ocr_dir, "reason": "OCR JSON directory is missing"})
