from app.modules.transcription.engine import SpeechEngine
from app.core.settings import settings
from loguru import logger

class AudioTranscriber:
    """Handles triggering the transcription model against the audio file."""
    
    @staticmethod
    def transcribe(audio_path: str):
        """Executes the Whisper model on the audio and returns segments and info."""
        engine = SpeechEngine.get_instance()
        try:
            language_setting = None if settings.WHISPER_LANGUAGE == "auto" else settings.WHISPER_LANGUAGE
            
            segments, info = engine.transcribe(
                audio_path,
                language=language_setting,
                beam_size=settings.WHISPER_BEAM_SIZE,
                vad_filter=settings.WHISPER_VAD_FILTER
            )
            
            return segments, info
            
        except Exception as e:
            logger.error(f"Transcription inference failed for {audio_path}: {str(e)}")
            raise e
