class CodeDetector:
    """Lightweight filter to avoid LLM calls on obvious non-code content."""
    
    @staticmethod
    def contains_code(chunk: dict) -> bool:
        # For maximum accuracy, we rely on the LLM to detect code.
        # This function acts as a placeholder if we want to add regex heuristics later.
        return True
