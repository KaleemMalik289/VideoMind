from app.modules.transcription.schemas import TranscriptSegment
from app.modules.transcription.cleaner import TranscriptCleaner
from loguru import logger

class TranscriptParser:
    """Parses raw Faster-Whisper segments into structured schemas."""
    
    @staticmethod
    def parse_segments(raw_segments) -> list[TranscriptSegment]:
        """Extracts and sanitizes Whisper segments."""
        parsed = []
        segment_id = 1
        
        for segment in raw_segments:
            cleaned_text = TranscriptCleaner.clean_text(segment.text)
            
            # Skip empty segments
            if not cleaned_text:
                continue
                
            parsed.append(TranscriptSegment(
                segment_id=segment_id,
                start=round(segment.start, 2),
                end=round(segment.end, 2),
                text=cleaned_text
            ))
            segment_id += 1
            
        return parsed
