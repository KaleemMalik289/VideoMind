import httpx
from loguru import logger
from app.core.settings import settings
from app.modules.llm.providers.base import BaseLLMProvider
from app.modules.llm.exceptions import LLMError

class GeminiProvider(BaseLLMProvider):
    """Handles Google Gemini via their REST API (v1beta) to avoid large SDK dependencies."""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.LLM_MODEL
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
    def initialize(self) -> None:
        pass
        
    def generate(self, system_prompt: str, user_prompt: str) -> tuple[str, int]:
        payload = {
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [
                {
                    "parts": [{"text": user_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": settings.LLM_TEMPERATURE,
                "maxOutputTokens": settings.LLM_MAX_TOKENS,
                "topP": settings.LLM_TOP_P
            }
        }
        
        try:
            with httpx.Client(timeout=settings.LLM_TIMEOUT) as client:
                response = client.post(self.url, json=payload)
                response.raise_for_status()
                
                data = response.json()
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                tokens = data.get("usageMetadata", {}).get("totalTokenCount", 0)
                
                return content, tokens
                
        except Exception as e:
            logger.error(f"[GEMINI] API request failed: {str(e)}")
            raise LLMError(details={"error": str(e), "provider": "gemini"})
            
    def health_check(self) -> bool:
        return bool(self.api_key)
