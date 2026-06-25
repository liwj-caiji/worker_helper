from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# --- RawRecord ---
class RawRecordCreate(BaseModel):
    content: str
    source_type: str = "quick_note"


class RawRecordUpdate(BaseModel):
    content: str


class RawRecordOut(BaseModel):
    id: str
    content: str
    source_type: str
    recorded_at: datetime
    updated_at: datetime
    process_status: str

    model_config = {"from_attributes": True}


# --- ExperienceCard ---
class ExperienceCardOut(BaseModel):
    id: str
    title: str
    background: str
    tech_solution: str
    quantifiable_result: str
    reflection: str
    skill_tags: List[str]
    quality_score: int
    created_at: datetime
    processed_at: Optional[datetime]
    source_record_id: Optional[str]
    source_updated_at: Optional[datetime]
    metadata_: Optional[dict] = Field(serialization_alias="metadata", default=None)

    model_config = {"from_attributes": True}


class ExperienceCardUpdate(BaseModel):
    title: Optional[str] = None
    background: Optional[str] = None
    tech_solution: Optional[str] = None
    quantifiable_result: Optional[str] = None
    reflection: Optional[str] = None
    skill_tags: Optional[List[str]] = None


# --- SkillNode ---
class SkillNodeOut(BaseModel):
    id: str
    name: str
    category: str
    card_count: int
    proficiency: float

    model_config = {"from_attributes": True}


# --- Settings ---
class LLMSettingsUpdate(BaseModel):
    llm_provider: str
    llm_api_key: str
    llm_base_url: Optional[str] = None
    llm_model: str


class ReminderSettingsUpdate(BaseModel):
    reminder_enabled: bool
    reminder_time: str


# --- Coach ---
class CoachMessage(BaseModel):
    content: str
