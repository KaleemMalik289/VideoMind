import re

class OCRCleaner:
    """Cleans extracted OCR text while preserving its underlying meaning."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
            
        # Remove weird OCR artifacts or leading/trailing spaces
        cleaned = text.strip()
        
        # Replace multiple spaces with a single space
        cleaned = re.sub(r'[ ]{2,}', ' ', cleaned)
        
        return cleaned
