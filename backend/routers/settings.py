from fastapi import APIRouter
from datetime import datetime
from backend.config import settings
from backend.schemas import LLMSettingsUpdate, ReminderSettingsUpdate
from backend.llm.factory import reset_provider

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/llm")
def get_llm_settings():
    return {
        "llm_provider": settings.llm_provider,
        "llm_api_key": "***" + settings.llm_api_key.get_secret_value()[-4:] if len(settings.llm_api_key.get_secret_value()) > 4 else "",
        "llm_base_url": settings.llm_base_url,
        "llm_model": settings.llm_model,
    }


@router.put("/llm")
def update_llm_settings(data: LLMSettingsUpdate):
    from pydantic import SecretStr
    settings.llm_provider = data.llm_provider
    settings.llm_api_key = SecretStr(data.llm_api_key)
    settings.llm_base_url = data.llm_base_url
    settings.llm_model = data.llm_model
    reset_provider()
    return {"status": "ok", "message": "LLM settings updated. Provider reset."}


@router.get("/reminder")
def get_reminder_settings():
    return {
        "reminder_enabled": settings.reminder_enabled,
        "reminder_time": settings.reminder_time,
    }


@router.put("/reminder")
def update_reminder_settings(data: ReminderSettingsUpdate):
    settings.reminder_enabled = data.reminder_enabled
    settings.reminder_time = data.reminder_time
    return {"status": "ok", "message": "Reminder settings updated."}


@router.get("/reminder/status")
def get_reminder_status():
    now = datetime.now()
    hour, minute = map(int, settings.reminder_time.split(":"))
    window_start = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    window_end = window_start.replace(minute=minute + 10)
    in_window = window_start <= now <= window_end

    return {
        "should_remind": in_window and settings.reminder_enabled,
        "reminder_time": settings.reminder_time,
        "enabled": settings.reminder_enabled,
    }
