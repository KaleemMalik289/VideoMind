import threading
from loguru import logger
from faster_whisper import WhisperModel
from app.core.settings import settings

class SpeechEngine:
    """Singleton wrapper for Faster-Whisper to ensure it only loads into memory once."""
    
    _instance = None
    _lock = threading.Lock()
    
    @classmethod
    def get_instance(cls) -> WhisperModel:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    logger.info(f"Initializing Faster-Whisper Model ({settings.WHISPER_MODEL})...")
                    try:
                        cls._instance = WhisperModel(
                            model_size_or_path=settings.WHISPER_MODEL,
                            device=settings.WHISPER_DEVICE,
                            compute_type=settings.WHISPER_COMPUTE_TYPE
                        )
                        logger.info("Faster-Whisper initialized successfully.")
                    except Exception as e:
                        logger.error(f"Failed to initialize Faster-Whisper: {str(e)}")
                        raise e
        return cls._instance
