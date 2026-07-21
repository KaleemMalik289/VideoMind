import os
import cv2
from loguru import logger
from app.modules.ocr.exceptions import OCRValidationError

class ImageValidator:
    """Validates that a preprocessed frame is ready for OCR."""
    
    @staticmethod
    def validate(image_path: str) -> None:
        if not os.path.exists(image_path):
            logger.error(f"Missing image file: {image_path}")
            raise OCRValidationError(details={"path": image_path, "reason": "Missing file"})
            
        if os.path.getsize(image_path) == 0:
            logger.error(f"Empty image file: {image_path}")
            raise OCRValidationError(details={"path": image_path, "reason": "Empty file"})
            
        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"Corrupted or unsupported image file: {image_path}")
            raise OCRValidationError(details={"path": image_path, "reason": "Corrupted or unsupported format"})
