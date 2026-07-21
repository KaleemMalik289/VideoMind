import threading
from loguru import logger
from paddleocr import PaddleOCR
from app.core.settings import settings

class OCREngine:
    """Singleton wrapper for PaddleOCR to ensure it only loads into memory once."""
    
    _instance = None
    _lock = threading.Lock()
    
    @classmethod
    def get_instance(cls) -> PaddleOCR:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    logger.info("Initializing PaddleOCR Model...")
                    try:
                        cls._instance = PaddleOCR(
                            use_angle_cls=settings.OCR_ENABLE_ANGLE_CLASSIFIER,
                            lang=settings.OCR_LANGUAGE,
                            use_gpu=settings.OCR_USE_GPU,
                            show_log=False
                        )
                        logger.info("PaddleOCR initialized successfully.")
                    except Exception as e:
                        logger.error(f"Failed to initialize PaddleOCR: {str(e)}")
                        raise e
        return cls._instance
