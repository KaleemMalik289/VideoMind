from abc import ABC, abstractmethod
from typing import Tuple

class BaseLLMProvider(ABC):
    """Abstract interface for all LLM providers."""
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize clients or connections."""
        pass
        
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> Tuple[str, int]:
        """
        Sends the request to the LLM.
        Returns a tuple of (Response Content, Tokens Used).
        """
        pass
        
    @abstractmethod
    def health_check(self) -> bool:
        """Verifies API key and endpoint health."""
        pass
