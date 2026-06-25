from backend.config import settings
from backend.llm.base import LLMProvider
from backend.llm.claude_provider import ClaudeProvider
from backend.llm.openai_provider import OpenAIProvider


_provider: LLMProvider | None = None


def get_provider() -> LLMProvider:
    global _provider
    if _provider is None:
        _provider = _create_provider()
    return _provider


def reset_provider():
    global _provider
    _provider = None


def _create_provider() -> LLMProvider:
    api_key = settings.llm_api_key.get_secret_value()
    model = settings.llm_model
    base_url = settings.llm_base_url

    match settings.llm_provider:
        case "claude":
            return ClaudeProvider(api_key=api_key, model=model, base_url=base_url)
        case "openai":
            return OpenAIProvider(api_key=api_key, model=model, base_url=base_url)
        case _:
            raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
