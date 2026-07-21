from openai import OpenAI
from loguru import logger
from app.core.settings import settings
from app.modules.llm.providers.base import BaseLLMProvider
from app.modules.llm.exceptions import LLMError

class OpenAICompatibleProvider(BaseLLMProvider):
    """Handles OpenAI, Groq, OpenRouter, and Ollama using the official OpenAI client."""
    
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        self.client = None
        self.model = settings.LLM_MODEL
        
    def initialize(self) -> None:
        if self.provider_name == "openai":
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        elif self.provider_name == "groq":
            self.client = OpenAI(api_key=settings.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
        elif self.provider_name == "openrouter":
            self.client = OpenAI(api_key=settings.OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")
        elif self.provider_name == "ollama":
            self.client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
        else:
            raise ValueError(f"Unsupported OpenAI-compatible provider: {self.provider_name}")
            
    def generate(self, system_prompt: str, user_prompt: str) -> tuple[str, int]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                top_p=settings.LLM_TOP_P
            )
            
            content = response.choices[0].message.content
            tokens = response.usage.total_tokens if response.usage else 0
            
            return content, tokens
            
        except Exception as e:
            logger.error(f"[{self.provider_name.upper()}] API request failed: {str(e)}")
            raise LLMError(details={"error": str(e), "provider": self.provider_name})
            
    def health_check(self) -> bool:
        return self.client is not None
