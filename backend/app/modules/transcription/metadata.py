from app.core.settings import settings
from app.modules.transcription.schemas import TranscriptJSON, TranscriptMetadata
import time

class MetadataGenerator:
    """Generates transcript metadata."""
    
    @staticmethod
    def generate(job_id: str, transcript: TranscriptJSON, duration: float, processing_time: float) -> TranscriptMetadata:
        total_words = sum(len(seg.text.split()) for seg in transcript.segments)
        
        return TranscriptMetadata(
            job_id=job_id,
            audio_duration=duration,
            language=transcript.language,
            whisper_model=settings.WHISPER_MODEL,
            processing_time_sec=round(processing_time, 2),
            number_of_segments=len(transcript.segments),
            total_words=total_words
        )
