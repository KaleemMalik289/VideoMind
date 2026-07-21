import re

class TranscriptCleaner:
    """Cleans extracted audio text."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
            
        # Strip leading/trailing whitespaces
        cleaned = text.strip()
        
        # Replace multiple spaces with a single space
        cleaned = re.sub(r'[ ]{2,}', ' ', cleaned)
        
        return cleaned
