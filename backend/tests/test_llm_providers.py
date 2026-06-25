import pytest
from unittest.mock import patch, MagicMock
from pydantic import SecretStr
from backend.llm.base import LLMProvider
from backend.llm.factory import get_provider, reset_provider, _create_provider
from backend.config import settings


class FakeProvider(LLMProvider):
    def chat(self, system_prompt: str, user_message: str) -> str:
        return "fake response"


def test_fake_provider():
    p = FakeProvider()
    result = p.chat("you are helpful", "hello")
    assert result == "fake response"


def test_provider_factory_raises_on_unknown():
    settings.llm_provider = "unknown"
    reset_provider()
    with pytest.raises(ValueError, match="Unknown LLM provider"):
        _create_provider()
    settings.llm_provider = "claude"
    reset_provider()


def test_provider_singleton():
    reset_provider()
    settings.llm_provider = "claude"
    settings.llm_api_key = SecretStr("fake-key")
    with patch("backend.llm.factory.ClaudeProvider") as mock_cls:
        mock_cls.return_value = FakeProvider()
        p1 = get_provider()
        p2 = get_provider()
        assert p1 is p2
    reset_provider()
