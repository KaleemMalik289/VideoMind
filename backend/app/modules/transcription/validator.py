import os
import wave
from loguru import logger
from app.modules.transcription.exceptions import TranscriptionValidationError

class AudioValidator:
    """Validates that an audio file is ready for Whisper transcription."""
    
    @staticmethod
    def validate(audio_path: str) -> None:
        if not os.path.exists(audio_path):
            logger.error(f"Missing audio file: {audio_path}")
            raise TranscriptionValidationError(details={"path": audio_path, "reason": "Missing file"})
            
        if os.path.getsize(audio_path) == 0:
            logger.error(f"Empty audio file: {audio_path}")
            raise TranscriptionValidationError(details={"path": audio_path, "reason": "Empty file"})
            
        try:
            with wave.open(audio_path, 'rb') as wf:
                # Basic WAV validation
                channels = wf.getnchannels()
                rate = wf.getframerate()
                
                if channels == 0 or rate == 0:
                    raise ValueError("Invalid WAV header.")
        except Exception as e:
            logger.error(f"Corrupted or unsupported WAV file {audio_path}: {str(e)}")
            raise TranscriptionValidationError(details={"path": audio_path, "reason": "Corrupted or unsupported format"})
