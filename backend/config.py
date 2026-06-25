from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # LLM config
    llm_provider: str = "claude"
    llm_api_key: str = ""
    llm_base_url: Optional[str] = None
    llm_model: str = "claude-sonnet-4-6"

    # Reminder config
    reminder_enabled: bool = True
    reminder_time: str = "17:30"

    # Database
    database_url: str = "sqlite:///experience_factory.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
