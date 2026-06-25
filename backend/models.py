import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from backend.database import Base


def gen_id():
    return str(uuid.uuid4())


def utcnow():
    return datetime.now(timezone.utc)


class SourceType(str, enum.Enum):
    chat = "chat"
    quick_note = "quick_note"
    retrospective = "retrospective"


class ProcessStatus(str, enum.Enum):
    pending = "pending"
    processed = "processed"


class RawRecord(Base):
    __tablename__ = "raw_records"

    id = Column(String, primary_key=True, default=gen_id)
    content = Column(Text, nullable=False)
    source_type = Column(SAEnum(SourceType), nullable=False, default=SourceType.quick_note)
    recorded_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)
    process_status = Column(SAEnum(ProcessStatus), nullable=False, default=ProcessStatus.pending)

    card = relationship("ExperienceCard", back_populates="source_record", uselist=False)


class ExperienceCard(Base):
    __tablename__ = "experience_cards"

    id = Column(String, primary_key=True, default=gen_id)
    title = Column(String, nullable=False, default="")
    background = Column(Text, default="")
    tech_solution = Column(Text, default="")
    quantifiable_result = Column(Text, default="")
    reflection = Column(Text, default="")
    skill_tags = Column(JSON, default=list)
    quality_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    source_record_id = Column(String, ForeignKey("raw_records.id"), nullable=True)
    source_updated_at = Column(DateTime, nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)

    source_record = relationship("RawRecord", back_populates="card")


class SkillNode(Base):
    __tablename__ = "skill_nodes"

    id = Column(String, primary_key=True, default=gen_id)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, default="")
    card_count = Column(Integer, default=0)
    proficiency = Column(Float, default=0.0)
