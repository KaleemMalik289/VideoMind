import threading
from loguru import logger
from paddleocr import PaddleOCR
from app.core.settings import settings
from app.core.model_manager import model_manager

class OCREngine:
    """Singleton wrapper for PaddleOCR using the unified ModelManager."""
    
    @classmethod
    def get_instance(cls) -> PaddleOCR:
        return model_manager.get_ocr_model()
