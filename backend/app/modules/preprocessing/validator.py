import cv2
import os
from loguru import logger
from app.modules.preprocessing.exceptions import ImageValidationError

class ImageValidator:
    """Validates an image before it enters the preprocessing pipeline."""
    
    @staticmethod
    def validate(image_path: str) -> None:
        if not os.path.exists(image_path):
            logger.error(f"Missing image file: {image_path}")
            raise ImageValidationError(details={"path": image_path, "reason": "Missing file"})
            
        if os.path.getsize(image_path) == 0:
            logger.error(f"Empty image file: {image_path}")
            raise ImageValidationError(details={"path": image_path, "reason": "Empty file"})
            
        # Try reading to verify it isn't corrupted
        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"Corrupted or unsupported image file: {image_path}")
            raise ImageValidationError(details={"path": image_path, "reason": "Corrupted or unsupported format"})
