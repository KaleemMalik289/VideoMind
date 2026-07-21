from app.modules.ocr.engine import OCREngine
from loguru import logger

class TextDetector:
    """Handles triggering the OCR model and extracting raw bounding boxes and texts."""
    
    @staticmethod
    def run_ocr(image_path: str) -> list:
        """Executes the OCR engine on the image. PaddleOCR returns detection + recognition together."""
        engine = OCREngine.get_instance()
        try:
            # result is a list of lists: [[[box], (text, confidence)], ...]
            result = engine.ocr(image_path, cls=True)
            # if no text found, result might be [None]
            if not result or not result[0]:
                return []
            return result[0]
        except Exception as e:
            logger.error(f"OCR inference failed for {image_path}: {str(e)}")
            raise e
