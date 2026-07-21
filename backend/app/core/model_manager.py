import threading
from loguru import logger
from app.core.settings import settings

class ModelManager:
    _instance = None
    _lock = threading.Lock()
    
    _ocr_model = None
    _whisper_model = None
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance
        
    def get_ocr_model(self):
        if not settings.ENABLE_MODEL_SINGLETON:
            from paddleocr import PaddleOCR
            logger.info("Initializing non-singleton PaddleOCR model")
            return PaddleOCR(use_angle_cls=True, lang='en')
            
        if self._ocr_model is None:
            with self._lock:
                if self._ocr_model is None:
                    logger.info("Lazy loading Singleton PaddleOCR model...")
                    from paddleocr import PaddleOCR
                    self._ocr_model = PaddleOCR(use_angle_cls=True, lang='en')
                    logger.info("Singleton PaddleOCR model loaded successfully.")
        return self._ocr_model

    def get_whisper_model(self):
        if not settings.ENABLE_MODEL_SINGLETON:
            from faster_whisper import WhisperModel
            logger.info("Initializing non-singleton Faster-Whisper model")
            return WhisperModel(model_size_or_path="base", device="cpu", compute_type="int8")
            
        if self._whisper_model is None:
            with self._lock:
                if self._whisper_model is None:
                    logger.info("Lazy loading Singleton Faster-Whisper model...")
                    from faster_whisper import WhisperModel
                    self._whisper_model = WhisperModel(model_size_or_path="base", device="cpu", compute_type="int8")
                    logger.info("Singleton Faster-Whisper model loaded successfully.")
        return self._whisper_model

model_manager = ModelManager()
