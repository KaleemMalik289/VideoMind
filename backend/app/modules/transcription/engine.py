import threading
from loguru import logger
from faster_whisper import WhisperModel
from app.core.settings import settings
from app.core.model_manager import model_manager

class SpeechEngine:
    """Singleton wrapper for Faster-Whisper using the unified ModelManager."""
    
    @classmethod
    def get_instance(cls) -> WhisperModel:
        return model_manager.get_whisper_model()
