from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def chat(self, system_prompt: str, user_message: str) -> str:
        """Send a chat request and return the text response."""
        ...
