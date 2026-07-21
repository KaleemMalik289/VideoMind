from rapidfuzz import fuzz
from loguru import logger

class TextDeduplicator:
    """Removes visually duplicate OCR frames across consecutive sequence segments using fuzzy matching."""
    
    @staticmethod
    def is_duplicate(text1: str, text2: str, threshold: float = 95.0) -> bool:
        """Returns True if the string similarity exceeds the threshold."""
        if not text1 and not text2:
            return True
        if not text1 or not text2:
            return False
            
        ratio = fuzz.ratio(text1, text2)
        return ratio >= threshold
        
    @staticmethod
    def deduplicate_transcript(transcript1: str, transcript2: str, threshold: float = 95.0) -> bool:
        """Returns True if transcripts are fundamentally identical."""
        return TextDeduplicator.is_duplicate(transcript1, transcript2, threshold)
