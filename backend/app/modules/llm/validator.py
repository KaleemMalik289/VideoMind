import os
from loguru import logger
from app.core.settings import settings
from app.modules.llm.exceptions import LLMValidationError

class LLMValidator:
    """Validates that semantic chunks exist and the configured API key is present."""
    
    @staticmethod
    def validate(chunks_path: str) -> None:
        if not os.path.exists(chunks_path):
            logger.error(f"Missing chunks file: {chunks_path}")
            raise LLMValidationError(details={"path": chunks_path, "reason": "Chunks JSON is missing"})
            
        provider = settings.LLM_PROVIDER.lower()
        if provider == "groq" and not settings.GROQ_API_KEY:
            raise LLMValidationError(details={"reason": "GROQ_API_KEY is not set"})
        elif provider == "openai" and not settings.OPENAI_API_KEY:
            raise LLMValidationError(details={"reason": "OPENAI_API_KEY is not set"})
        elif provider == "gemini" and not settings.GEMINI_API_KEY:
            raise LLMValidationError(details={"reason": "GEMINI_API_KEY is not set"})
        elif provider == "openrouter" and not settings.OPENROUTER_API_KEY:
            raise LLMValidationError(details={"reason": "OPENROUTER_API_KEY is not set"})
