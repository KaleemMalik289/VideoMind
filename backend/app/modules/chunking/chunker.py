class TokenEstimator:
    """Estimates LLM tokens using a lightweight heuristic to avoid heavy tiktoken dependencies."""
    
    @staticmethod
    def estimate(text: str) -> int:
        if not text:
            return 0
        # 1 word ~ 1.3 tokens in English LLM encoding
        return int(len(text.split()) * 1.3)

class SemanticChunker:
    """Evaluates when a chunk has reached sufficient context density to be sliced."""
    
    @staticmethod
    def estimate_entry_tokens(entry: dict) -> int:
        tokens = 0
        tokens += TokenEstimator.estimate(entry.get("transcript", ""))
        for text in entry.get("ocr_text", []):
            tokens += TokenEstimator.estimate(text)
        return tokens
