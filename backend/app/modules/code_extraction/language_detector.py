class LanguageDetector:
    """Detects programming language from reconstructed code."""
    
    @staticmethod
    def detect(code: str) -> str:
        # LLM provides this in CodeJSON. This could be used as a fallback.
        # But we rely on the LLM's 'language' field from the merger response.
        return "Unknown"
