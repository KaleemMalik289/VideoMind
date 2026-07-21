from app.core.settings import settings
from app.modules.llm.providers.base import BaseLLMProvider
from app.modules.llm.providers.openai_provider import OpenAICompatibleProvider
from app.modules.llm.providers.gemini_provider import GeminiProvider

class ProviderFactory:
    @staticmethod
    def get_provider() -> BaseLLMProvider:
        provider_name = settings.LLM_PROVIDER.lower()
        
        if provider_name in ["openai", "groq", "openrouter", "ollama"]:
            provider = OpenAICompatibleProvider(provider_name)
        elif provider_name == "gemini":
            provider = GeminiProvider()
        else:
            raise ValueError(f"Unknown LLM provider configured: {provider_name}")
            
        provider.initialize()
        return provider
