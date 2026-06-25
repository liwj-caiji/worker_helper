# 经验工厂 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an AI-driven personal work experience accumulation system — capture, process, store, and browse structured experience cards with proactive reminders.

**Architecture:** Python FastAPI backend with Vue 3 frontend. Four-layer pipeline (Capture → Process → Store → Generate) with a cross-cutting guidance system. LLM access via provider adapter pattern for model-swappable AI processing.

**Tech Stack:** Python 3.12+, FastAPI, SQLAlchemy + SQLite, APScheduler, Vue 3 + Vite + Tailwind CSS, Anthropic Claude API (default LLM)

---

## File Structure

```
worker_helper/
├── backend/
│   ├── main.py                      # FastAPI app, CORS, router registration
│   ├── config.py                    # Settings from env/file: LLM config, reminders
│   ├── database.py                  # SQLAlchemy engine, session, Base
│   ├── models.py                    # All ORM models in one file (MVP scale)
│   ├── schemas.py                   # All Pydantic schemas in one file
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py                  # LLMProvider abstract class
│   │   ├── claude_provider.py       # Anthropic Claude implementation
│   │   ├── openai_provider.py       # OpenAI GPT implementation
│   │   └── factory.py              # get_provider() from config
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pipeline.py             # AI processing pipeline
│   │   ├── coach.py                # Coach conversation logic
│   │   └── reminder.py             # Scheduled reminder service
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── records.py              # RawRecord endpoints
│   │   ├── cards.py                # ExperienceCard endpoints
│   │   ├── coach.py                # Coach chat endpoint
│   │   └── settings.py             # Config endpoints
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_models.py
│       ├── test_llm_providers.py
│       ├── test_pipeline.py
│       ├── test_coach.py
│       ├── test_records_api.py
│       ├── test_cards_api.py
│       └── test_settings_api.py
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── style.css
│       ├── router/index.js
│       ├── api/index.js
│       ├── store/index.js           # Pinia store
│       ├── views/
│       │   ├── CoachView.vue
│       │   ├── CardsView.vue
│       │   ├── CardDetailView.vue
│       │   ├── RecordsView.vue
│       │   ├── RecordEditView.vue
│       │   └── SettingsView.vue
│       └── components/
│           ├── AppLayout.vue
│           ├── SideNav.vue
│           ├── QuickNotePanel.vue
│           ├── ReminderPopup.vue
│           ├── CoachChat.vue
│           ├── CardList.vue
│           ├── CardDetail.vue
│           ├── RecordList.vue
│           └── SettingsPanel.vue
└── requirements.txt
```

---

## Phase 1: Project Scaffolding & Infrastructure

### Task 1: Initialize project structure and git

**Files:**
- Create: `requirements.txt`
- Create: `backend/__init__.py`

- [ ] **Step 1: Create requirements.txt**

```txt
fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy==2.0.35
aiosqlite==0.20.0
apscheduler==3.10.4
pydantic==2.9.2
pydantic-settings==2.5.2
anthropic==0.34.0
openai==1.51.0
python-dotenv==1.0.1
pytest==8.3.3
httpx==0.27.2
```

- [ ] **Step 2: Create backend package init**

```python
# backend/__init__.py
```

- [ ] **Step 3: Initialize git and commit**

```bash
cd /c/Users/liwenjie/Desktop/workspace/worker_helper
git init
echo ".superpowers/" > .gitignore
echo "__pycache__/" >> .gitignore
echo ".venv/" >> .gitignore
echo "node_modules/" >> .gitignore
echo "*.db" >> .gitignore
echo ".env" >> .gitignore
git add -A
git commit -m "chore: initialize project structure"
```

### Task 2: Set up Python environment and install dependencies

- [ ] **Step 1: Create virtual environment and install**

```bash
cd /c/Users/liwenjie/Desktop/workspace/worker_helper
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

- [ ] **Step 2: Commit lock file**

```bash
pip freeze > requirements-lock.txt
git add requirements-lock.txt
git commit -m "chore: add dependency lock file"
```

### Task 3: Create database module

**Files:**
- Create: `backend/database.py`

- [ ] **Step 1: Write database.py**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///experience_factory.db"

engine = create_engine(
    DATABASE_URL.replace("+aiosqlite", ""),
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
```

- [ ] **Step 2: Commit**

```bash
git add backend/database.py
git commit -m "feat: add database module with SQLAlchemy setup"
```

### Task 4: Create config module

**Files:**
- Create: `backend/config.py`

- [ ] **Step 1: Write config.py**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add backend/config.py
git commit -m "feat: add config module with LLM and reminder settings"
```

### Task 5: Create FastAPI app entry point

**Files:**
- Create: `backend/main.py`

- [ ] **Step 1: Write main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db

app = FastAPI(title="Experience Factory")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok"}
```

- [ ] **Step 2: Verify server starts**

```bash
cd /c/Users/liwenjie/Desktop/workspace/worker_helper
source .venv/Scripts/activate
uvicorn backend.main:app --reload --port 8000 &
sleep 3
curl http://localhost:8000/api/health
# Expected: {"status":"ok"}
kill %1
```

- [ ] **Step 3: Commit**

```bash
git add backend/main.py
git commit -m "feat: add FastAPI app entry point with CORS and health check"
```

---

## Phase 2: Data Models

### Task 6: Create ORM models

**Files:**
- Create: `backend/models.py`

- [ ] **Step 1: Write models.py**

```python
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
```

- [ ] **Step 2: Write test_models.py**

```python
import pytest
from backend.database import init_db, SessionLocal, Base, engine
from backend.models import RawRecord, ExperienceCard, SkillNode, SourceType, ProcessStatus, gen_id


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_raw_record():
    db = SessionLocal()
    record = RawRecord(content="优化了查询性能", source_type=SourceType.quick_note)
    db.add(record)
    db.commit()
    db.refresh(record)
    assert record.id is not None
    assert record.content == "优化了查询性能"
    assert record.source_type == SourceType.quick_note
    assert record.process_status == ProcessStatus.pending
    db.close()


def test_create_experience_card():
    db = SessionLocal()
    record = RawRecord(content="测试内容", source_type=SourceType.chat)
    db.add(record)
    db.commit()

    card = ExperienceCard(
        title="测试卡片",
        tech_solution="使用了缓存",
        quantifiable_result="性能提升50%",
        skill_tags=["缓存", "性能优化"],
        source_record_id=record.id,
        quality_score=80,
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    assert card.title == "测试卡片"
    assert card.source_record_id == record.id
    assert "缓存" in card.skill_tags
    db.close()


def test_create_skill_node():
    db = SessionLocal()
    node = SkillNode(name="Python", category="编程语言", card_count=5, proficiency=0.8)
    db.add(node)
    db.commit()
    db.refresh(node)
    assert node.name == "Python"
    assert node.proficiency == 0.8
    db.close()
```

- [ ] **Step 3: Run tests**

```bash
cd /c/Users/liwenjie/Desktop/workspace/worker_helper
source .venv/Scripts/activate
python -m pytest backend/tests/test_models.py -v
# Expected: 3 passed
```

- [ ] **Step 4: Commit**

```bash
git add backend/models.py backend/tests/test_models.py
git commit -m "feat: add ORM models for RawRecord, ExperienceCard, SkillNode"
```

### Task 7: Create Pydantic schemas

**Files:**
- Create: `backend/schemas.py`

- [ ] **Step 1: Write schemas.py**

```python
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
    metadata_: Optional[dict] = Field(alias="metadata", default=None)

    model_config = {"from_attributes": True, "populate_by_name": True}


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
```

- [ ] **Step 2: Commit**

```bash
git add backend/schemas.py
git commit -m "feat: add Pydantic schemas for API request/response"
```

---

## Phase 3: LLM Provider Abstraction

### Task 8: Create LLM provider base and implementations

**Files:**
- Create: `backend/llm/__init__.py`
- Create: `backend/llm/base.py`
- Create: `backend/llm/claude_provider.py`
- Create: `backend/llm/openai_provider.py`
- Create: `backend/llm/factory.py`

- [ ] **Step 1: Write llm/__init__.py**

```python
from backend.llm.factory import get_provider
```

- [ ] **Step 2: Write llm/base.py**

```python
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def chat(self, system_prompt: str, user_message: str) -> str:
        """Send a chat request and return the text response."""
        ...
```

- [ ] **Step 3: Write llm/claude_provider.py**

```python
from anthropic import Anthropic
from backend.llm.base import LLMProvider


class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6", base_url: str | None = None):
        kwargs = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self.client = Anthropic(**kwargs)
        self.model = model

    def chat(self, system_prompt: str, user_message: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text
```

- [ ] **Step 4: Write llm/openai_provider.py**

```python
from openai import OpenAI
from backend.llm.base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o", base_url: str | None = None):
        kwargs = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self.client = OpenAI(**kwargs)
        self.model = model

    def chat(self, system_prompt: str, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=2048,
        )
        return response.choices[0].message.content
```

- [ ] **Step 5: Write llm/factory.py**

```python
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
    api_key = settings.llm_api_key
    model = settings.llm_model
    base_url = settings.llm_base_url

    match settings.llm_provider:
        case "claude":
            return ClaudeProvider(api_key=api_key, model=model, base_url=base_url)
        case "openai":
            return OpenAIProvider(api_key=api_key, model=model, base_url=base_url)
        case _:
            raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
```

- [ ] **Step 6: Write test_llm_providers.py**

```python
import pytest
from unittest.mock import patch, MagicMock
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
    # restore
    settings.llm_provider = "claude"
    reset_provider()


def test_provider_singleton():
    reset_provider()
    settings.llm_provider = "claude"
    settings.llm_api_key = "fake-key"
    with patch("backend.llm.factory.ClaudeProvider") as mock_cls:
        mock_cls.return_value = FakeProvider()
        p1 = get_provider()
        p2 = get_provider()
        assert p1 is p2
    reset_provider()
```

- [ ] **Step 7: Run tests**

```bash
python -m pytest backend/tests/test_llm_providers.py -v
# Expected: 3 passed
```

- [ ] **Step 8: Commit**

```bash
git add backend/llm/ backend/tests/test_llm_providers.py
git commit -m "feat: add LLM provider abstraction with Claude and OpenAI implementations"
```

---

## Phase 4: AI Processing Pipeline

### Task 9: Create processing pipeline service

**Files:**
- Create: `backend/services/__init__.py`
- Create: `backend/services/pipeline.py`

- [ ] **Step 1: Write services/__init__.py**

```python
```

- [ ] **Step 2: Write services/pipeline.py**

```python
import json
from datetime import datetime, timezone
from backend.llm import get_provider
from backend.models import RawRecord, ExperienceCard, SkillNode, ProcessStatus, utcnow
from backend.schemas import ExperienceCardUpdate

EXTRACTION_PROMPT = """You are an expert career coach. Extract structured work experience from the user's raw input.

Return ONLY valid JSON with these fields:
{
  "title": "short summary of the achievement (max 30 chars)",
  "background": "context: when, which project, your role",
  "tech_solution": "technical approach, tools, methods used",
  "quantifiable_result": "measurable outcome with numbers if possible. If user didn't provide numbers, suggest reasonable metrics they could track",
  "reflection": "what was learned, what could be improved. If not mentioned, leave empty string",
  "skill_tags": ["tag1", "tag2"]
}

User's raw input:"""

SCORING_PROMPT = """Rate this experience card on completeness (0-100). Consider:
- Has specific project context? (25pts)
- Has technical details? (25pts)
- Has measurable result? (25pts)
- Has reflection/learning? (25pts)

Return ONLY a number. No explanation.

Card:
"""


def process_record(db_session, record: RawRecord) -> ExperienceCard:
    """Run the AI processing pipeline on a raw record, producing/updating an experience card."""
    provider = get_provider()

    # Step 1: Extract structured data
    extraction_result = provider.chat(EXTRACTION_PROMPT, record.content)
    data = json.loads(extraction_result)

    # Step 2: Score quality
    card_text = f"Title: {data['title']}\nBackground: {data['background']}\nTech: {data['tech_solution']}\nResult: {data['quantifiable_result']}\nReflection: {data['reflection']}"
    score_str = provider.chat(SCORING_PROMPT, card_text)
    quality_score = int(score_str.strip())

    # Step 3: Upsert experience card
    existing = db_session.query(ExperienceCard).filter(
        ExperienceCard.source_record_id == record.id
    ).first()

    now = utcnow()
    if existing:
        existing.title = data["title"]
        existing.background = data["background"]
        existing.tech_solution = data["tech_solution"]
        existing.quantifiable_result = data["quantifiable_result"]
        existing.reflection = data["reflection"]
        existing.skill_tags = data["skill_tags"]
        existing.quality_score = quality_score
        existing.processed_at = now
        existing.source_updated_at = record.updated_at
        card = existing
    else:
        card = ExperienceCard(
            title=data["title"],
            background=data["background"],
            tech_solution=data["tech_solution"],
            quantifiable_result=data["quantifiable_result"],
            reflection=data["reflection"],
            skill_tags=data["skill_tags"],
            quality_score=quality_score,
            source_record_id=record.id,
            source_updated_at=record.updated_at,
            processed_at=now,
        )
        db_session.add(card)

    # Step 4: Update or create skill nodes
    for tag in data["skill_tags"]:
        node = db_session.query(SkillNode).filter(SkillNode.name == tag).first()
        if node:
            node.card_count += 1
        else:
            node = SkillNode(name=tag, category="", card_count=1, proficiency=0.0)
            db_session.add(node)

    # Step 5: Mark record as processed
    record.process_status = ProcessStatus.processed

    db_session.commit()
    db_session.refresh(card)
    return card
```

- [ ] **Step 3: Write test_pipeline.py**

```python
import pytest
from unittest.mock import patch, MagicMock
from backend.database import SessionLocal, Base, engine
from backend.models import RawRecord, ExperienceCard, SkillNode, SourceType, ProcessStatus
from backend.services.pipeline import process_record


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def fake_provider():
    mock = MagicMock()
    mock.chat.side_effect = [
        '{"title":"查询性能优化","background":"Q2 交易系统后端","tech_solution":"Redis缓存热点查询","quantifiable_result":"查询耗时 2.3s -> 180ms","reflection":"要注意缓存穿透","skill_tags":["Redis","性能优化"]}',
        "85",
    ]
    return mock


def test_process_record_creates_card():
    db = SessionLocal()
    record = RawRecord(content="优化了订单查询", source_type=SourceType.chat)
    db.add(record)
    db.commit()
    db.refresh(record)

    with patch("backend.services.pipeline.get_provider", return_value=fake_provider()):
        card = process_record(db, record)

    assert card.title == "查询性能优化"
    assert "Redis" in card.skill_tags
    assert card.quality_score == 85
    assert card.source_record_id == record.id

    db.refresh(record)
    assert record.process_status == ProcessStatus.processed

    node = db.query(SkillNode).filter(SkillNode.name == "Redis").first()
    assert node is not None
    assert node.card_count == 1
    db.close()


def test_process_record_updates_existing_card():
    db = SessionLocal()
    record = RawRecord(content="v1", source_type=SourceType.quick_note)
    db.add(record)
    db.commit()
    db.refresh(record)

    with patch("backend.services.pipeline.get_provider", return_value=fake_provider()):
        card1 = process_record(db, record)
        # Edit raw record and re-process
        record.content = "v2 updated"
        card2 = process_record(db, record)

    assert card1.id == card2.id
    assert card2.quality_score == 85
    db.close()
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest backend/tests/test_pipeline.py -v
# Expected: 2 passed
```

- [ ] **Step 5: Commit**

```bash
git add backend/services/ backend/tests/test_pipeline.py
git commit -m "feat: add AI processing pipeline for raw record to experience card"
```

---

## Phase 5: API Endpoints

### Task 10: Create raw records API

**Files:**
- Create: `backend/routers/__init__.py`
- Create: `backend/routers/records.py`

- [ ] **Step 1: Write routers/__init__.py**

```python
```

- [ ] **Step 2: Write routers/records.py**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import RawRecord
from backend.schemas import RawRecordCreate, RawRecordUpdate, RawRecordOut
from backend.services.pipeline import process_record

router = APIRouter(prefix="/api/records", tags=["records"])


@router.post("", response_model=RawRecordOut, status_code=201)
def create_record(data: RawRecordCreate, db: Session = Depends(get_db)):
    record = RawRecord(content=data.content, source_type=data.source_type)
    db.add(record)
    db.commit()
    db.refresh(record)
    # Trigger async processing? For MVP, process synchronously
    if record.content.strip():
        process_record(db, record)
        db.refresh(record)
    return record


@router.get("", response_model=List[RawRecordOut])
def list_records(
    source_type: str | None = None,
    process_status: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(RawRecord)
    if source_type:
        q = q.filter(RawRecord.source_type == source_type)
    if process_status:
        q = q.filter(RawRecord.process_status == process_status)
    return q.order_by(RawRecord.recorded_at.desc()).all()


@router.get("/{record_id}", response_model=RawRecordOut)
def get_record(record_id: str, db: Session = Depends(get_db)):
    record = db.query(RawRecord).filter(RawRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@router.put("/{record_id}", response_model=RawRecordOut)
def update_record(record_id: str, data: RawRecordUpdate, db: Session = Depends(get_db)):
    record = db.query(RawRecord).filter(RawRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    record.content = data.content
    db.commit()
    db.refresh(record)
    # Re-process to update the associated card
    process_record(db, record)
    db.refresh(record)
    return record


@router.delete("/{record_id}", status_code=204)
def delete_record(record_id: str, db: Session = Depends(get_db)):
    record = db.query(RawRecord).filter(RawRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(record)
    db.commit()
    return None
```

- [ ] **Step 3: Write test_records_api.py**

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.database import Base, engine, get_db, SessionLocal
from backend.main import app
from backend.models import RawRecord, SourceType


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def fake_provider():
    mock = MagicMock()
    mock.chat.side_effect = [
        '{"title":"测试","background":"bg","tech_solution":"tech","quantifiable_result":"result","reflection":"","skill_tags":["Tag1"]}',
        "70",
        '{"title":"测试更新","background":"bg2","tech_solution":"tech2","quantifiable_result":"result2","reflection":"r2","skill_tags":["Tag2"]}',
        "75",
    ]
    return mock


def test_create_record(client):
    with patch("backend.services.pipeline.get_provider", return_value=fake_provider()):
        resp = client.post("/api/records", json={"content": "测试输入", "source_type": "chat"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["content"] == "测试输入"
    assert data["process_status"] == "processed"


def test_list_records(client):
    with patch("backend.services.pipeline.get_provider", return_value=fake_provider()):
        client.post("/api/records", json={"content": "记录1", "source_type": "chat"})
        client.post("/api/records", json={"content": "记录2", "source_type": "quick_note"})
    resp = client.get("/api/records")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_record(client):
    with patch("backend.services.pipeline.get_provider", return_value=fake_provider()):
        create_resp = client.post("/api/records", json={"content": "测试", "source_type": "chat"})
        record_id = create_resp.json()["id"]
    resp = client.get(f"/api/records/{record_id}")
    assert resp.status_code == 200
    assert resp.json()["content"] == "测试"


def test_update_record(client):
    with patch("backend.services.pipeline.get_provider", return_value=fake_provider()):
        create_resp = client.post("/api/records", json={"content": "原始", "source_type": "chat"})
        record_id = create_resp.json()["id"]
        resp = client.put(f"/api/records/{record_id}", json={"content": "已更新"})
    assert resp.status_code == 200
    assert resp.json()["content"] == "已更新"


def test_delete_record(client):
    with patch("backend.services.pipeline.get_provider", return_value=fake_provider()):
        create_resp = client.post("/api/records", json={"content": "待删除", "source_type": "chat"})
        record_id = create_resp.json()["id"]
    resp = client.delete(f"/api/records/{record_id}")
    assert resp.status_code == 204
    resp = client.get(f"/api/records/{record_id}")
    assert resp.status_code == 404
```

- [ ] **Step 4: Register router in main.py**

Modify `backend/main.py` — add after the health endpoint and before app definition ends:

```python
from backend.routers import records

app.include_router(records.router)
```

- [ ] **Step 5: Run tests**

```bash
python -m pytest backend/tests/test_records_api.py -v
# Expected: 5 passed
```

- [ ] **Step 6: Commit**

```bash
git add backend/routers/ backend/main.py backend/tests/test_records_api.py
git commit -m "feat: add raw records CRUD API with AI processing on create/update"
```

### Task 11: Create experience cards API

**Files:**
- Create: `backend/routers/cards.py`

- [ ] **Step 1: Write routers/cards.py**

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import ExperienceCard
from backend.schemas import ExperienceCardOut, ExperienceCardUpdate

router = APIRouter(prefix="/api/cards", tags=["cards"])


@router.get("", response_model=List[ExperienceCardOut])
def list_cards(
    skill_tag: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(ExperienceCard)
    if skill_tag:
        q = q.filter(ExperienceCard.skill_tags.contains(skill_tag))
    if search:
        q = q.filter(
            (ExperienceCard.title.contains(search)) |
            (ExperienceCard.tech_solution.contains(search))
        )
    return q.order_by(ExperienceCard.created_at.desc()).all()


@router.get("/{card_id}", response_model=ExperienceCardOut)
def get_card(card_id: str, db: Session = Depends(get_db)):
    card = db.query(ExperienceCard).filter(ExperienceCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.put("/{card_id}", response_model=ExperienceCardOut)
def update_card(card_id: str, data: ExperienceCardUpdate, db: Session = Depends(get_db)):
    card = db.query(ExperienceCard).filter(ExperienceCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(card, field, value)
    db.commit()
    db.refresh(card)
    return card
```

- [ ] **Step 2: Write test_cards_api.py**

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.database import Base, engine
from backend.main import app
from backend.models import ExperienceCard, RawRecord


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def fake_provider():
    mock = MagicMock()
    mock.chat.side_effect = [
        '{"title":"优化查询","background":"订单系统","tech_solution":"Redis缓存","quantifiable_result":"查询提速90%","reflection":"注意过期策略","skill_tags":["Redis","性能"]}',
        "80",
    ]
    return mock


@pytest.fixture
def seeded_card(client):
    with patch("backend.services.pipeline.get_provider", return_value=fake_provider()):
        client.post("/api/records", json={"content": "做了优化", "source_type": "chat"})
    resp = client.get("/api/cards")
    cards = resp.json()
    return cards[0]


def test_list_cards(client, seeded_card):
    resp = client.get("/api/cards")
    assert resp.status_code == 200
    cards = resp.json()
    assert len(cards) >= 1
    assert cards[0]["title"] == "优化查询"


def test_filter_cards_by_tag(client, seeded_card):
    resp = client.get("/api/cards?skill_tag=Redis")
    assert resp.status_code == 200
    cards = resp.json()
    assert len(cards) >= 1


def test_search_cards(client, seeded_card):
    resp = client.get("/api/cards?search=缓存")
    assert resp.status_code == 200
    cards = resp.json()
    assert len(cards) >= 1


def test_get_card(client, seeded_card):
    resp = client.get(f"/api/cards/{seeded_card['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "优化查询"


def test_update_card(client, seeded_card):
    resp = client.put(f"/api/cards/{seeded_card['id']}", json={"title": "新标题"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "新标题"


def test_get_nonexistent_card(client):
    resp = client.get("/api/cards/nonexistent")
    assert resp.status_code == 404
```

- [ ] **Step 3: Register cards router in main.py**

Add in `backend/main.py`:
```python
from backend.routers import cards

app.include_router(cards.router)
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest backend/tests/test_cards_api.py -v
# Expected: 6 passed
```

- [ ] **Step 5: Commit**

```bash
git add backend/routers/cards.py backend/main.py backend/tests/test_cards_api.py
git commit -m "feat: add experience cards API with search and skill-tag filtering"
```

### Task 12: Create coach chat endpoint

**Files:**
- Create: `backend/services/coach.py`
- Create: `backend/routers/coach.py`

- [ ] **Step 1: Write services/coach.py**

```python
from backend.llm import get_provider

COACH_SYSTEM_PROMPT = """You are a friendly career coach helping a software engineer document their daily work experience.
Your goal: guide them to reflect on what they did, extract meaningful details.

Rules:
1. Keep it conversational. Ask one question at a time.
2. After they describe something, ask a follow-up to get specifics: what technology, what was the outcome, any numbers?
3. When they've provided enough detail (tech + outcome), acknowledge and suggest they've done a great job recording.
4. Always end with a question to keep the conversation going.
5. Be encouraging. This is for their own growth, not an interrogation.

Respond in Chinese (the user speaks Chinese)."""


def get_coach_response(user_message: str, conversation_history: list[dict] = None) -> str:
    """Generate the next coach message based on conversation context."""
    provider = get_provider()
    history = conversation_history or []
    messages = []
    for msg in history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    if len(messages) == 1:
        response = provider.chat(COACH_SYSTEM_PROMPT, user_message)
    else:
        full_context = "\n".join([f"{'用户' if m['role']=='user' else '教练'}: {m['content']}" for m in messages])
        response = provider.chat(COACH_SYSTEM_PROMPT, full_context)
    return response
```

- [ ] **Step 2: Write routers/coach.py**

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import RawRecord, SourceType
from backend.schemas import CoachMessage
from backend.services.coach import get_coach_response
from backend.services.pipeline import process_record

router = APIRouter(prefix="/api/coach", tags=["coach"])


@router.post("/chat")
def coach_chat(message: CoachMessage, db: Session = Depends(get_db)):
    """Send a message to the AI coach and get a response.
    The user's message is also saved as a raw record and processed."""
    # Save user message as a raw record
    record = RawRecord(content=message.content, source_type=SourceType.chat)
    db.add(record)
    db.commit()
    db.refresh(record)

    # Process in background (MVP: synchronous)
    if len(message.content.strip()) > 10:
        process_record(db, record)
        db.refresh(record)

    # Get coach response
    response = get_coach_response(message.content)
    return {"response": response, "record_id": record.id}
```

- [ ] **Step 3: Write test_coach.py**

```python
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.database import Base, engine
from backend.main import app


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def fake_provider():
    mock = MagicMock()
    mock.chat.side_effect = [
        # Pipeline extraction + scoring (2 calls)
        '{"title":"测试","background":"bg","tech_solution":"tech","quantifiable_result":"result","reflection":"","skill_tags":["Tag1"]}',
        "70",
        # Coach response (1 call)
        "听起来你今天做了很有价值的工作！能告诉我具体用到了什么技术吗？",
    ]
    return mock


def test_coach_chat(client):
    with patch("backend.services.pipeline.get_provider", return_value=fake_provider()):
        resp = client.post("/api/coach/chat", json={"content": "今天优化了数据库查询性能，速度提升明显"})
    assert resp.status_code == 200
    data = resp.json()
    assert "response" in data
    assert "record_id" in data
    assert "技术" in data["response"]
```

- [ ] **Step 4: Register coach router in main.py**

Add in `backend/main.py`:
```python
from backend.routers import coach

app.include_router(coach.router)
```

- [ ] **Step 5: Run tests**

```bash
python -m pytest backend/tests/test_coach.py -v
# Expected: 1 passed
```

- [ ] **Step 6: Commit**

```bash
git add backend/services/coach.py backend/routers/coach.py backend/main.py backend/tests/test_coach.py
git commit -m "feat: add coach chat endpoint with AI conversation and auto-recording"
```

### Task 13: Create settings API

**Files:**
- Create: `backend/routers/settings.py`

- [ ] **Step 1: Write routers/settings.py**

```python
from fastapi import APIRouter
from backend.config import settings
from backend.schemas import LLMSettingsUpdate, ReminderSettingsUpdate
from backend.llm.factory import reset_provider

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/llm")
def get_llm_settings():
    return {
        "llm_provider": settings.llm_provider,
        "llm_api_key": "***" + settings.llm_api_key[-4:] if len(settings.llm_api_key) > 4 else "",
        "llm_base_url": settings.llm_base_url,
        "llm_model": settings.llm_model,
    }


@router.put("/llm")
def update_llm_settings(data: LLMSettingsUpdate):
    settings.llm_provider = data.llm_provider
    settings.llm_api_key = data.llm_api_key
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
```

- [ ] **Step 2: Write test_settings_api.py**

```python
import pytest
from fastapi.testclient import TestClient
from backend.database import Base, engine
from backend.main import app
from backend.config import settings as cfg
from backend.llm.factory import reset_provider


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def test_get_llm_settings(client):
    resp = client.get("/api/settings/llm")
    assert resp.status_code == 200
    data = resp.json()
    assert "llm_provider" in data
    assert "llm_model" in data


def test_update_llm_settings(client):
    resp = client.put("/api/settings/llm", json={
        "llm_provider": "openai",
        "llm_api_key": "sk-test1234",
        "llm_base_url": None,
        "llm_model": "gpt-4o",
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert cfg.llm_provider == "openai"
    reset_provider()


def test_get_reminder_settings(client):
    resp = client.get("/api/settings/reminder")
    assert resp.status_code == 200
    assert "reminder_enabled" in resp.json()


def test_update_reminder_settings(client):
    resp = client.put("/api/settings/reminder", json={
        "reminder_enabled": True,
        "reminder_time": "09:00",
    })
    assert resp.status_code == 200
```

- [ ] **Step 3: Register settings router in main.py**

Add in `backend/main.py`:
```python
from backend.routers import settings as settings_router

app.include_router(settings_router.router)
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest backend/tests/test_settings_api.py -v
# Expected: 4 passed
```

- [ ] **Step 5: Commit**

```bash
git add backend/routers/settings.py backend/main.py backend/tests/test_settings_api.py
git commit -m "feat: add settings API for LLM and reminder configuration"
```

---

## Phase 6: Reminder System

### Task 14: Create reminder service with APScheduler

**Files:**
- Create: `backend/services/reminder.py`

- [ ] **Step 1: Write services/reminder.py**

```python
from apscheduler.schedulers.background import BackgroundScheduler
from backend.config import settings

scheduler = BackgroundScheduler()


def _reminder_job():
    """This job runs at configured times. In MVP, it just logs.
    The frontend polls a status endpoint to decide whether to show the popup."""
    pass  # Actual notification will be polled by frontend


def start_scheduler():
    if not scheduler.running:
        hour, minute = settings.reminder_time.split(":")
        scheduler.add_job(
            _reminder_job,
            "cron",
            hour=int(hour),
            minute=int(minute),
            id="daily_reminder",
        )
        scheduler.start()


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
```

- [ ] **Step 2: Add reminder status endpoint in routers/settings.py**

Add to `backend/routers/settings.py`:
```python
from datetime import datetime
from backend.services.reminder import scheduler


@router.get("/reminder/status")
def get_reminder_status():
    """Frontend polls this to know if it should show the reminder popup."""
    now = datetime.now()
    hour, minute = map(int, settings.reminder_time.split(":"))
    # Show reminder within a 10-minute window of the configured time
    window_start = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    window_end = window_start.replace(minute=minute + 10)
    in_window = window_start <= now <= window_end

    return {
        "should_remind": in_window and settings.reminder_enabled,
        "reminder_time": settings.reminder_time,
        "enabled": settings.reminder_enabled,
    }
```

- [ ] **Step 3: Update main.py to start scheduler**

Add to `backend/main.py` after the startup event:
```python
from backend.services.reminder import start_scheduler, stop_scheduler


@app.on_event("startup")
def on_startup():
    init_db()
    start_scheduler()


@app.on_event("shutdown")
def on_shutdown():
    stop_scheduler()
```

- [ ] **Step 4: Commit**

```bash
git add backend/services/reminder.py backend/routers/settings.py backend/main.py
git commit -m "feat: add scheduled reminder service with configurable time"
```

---

## Phase 7: Frontend Scaffolding

### Task 15: Initialize Vue 3 + Vite project

- [ ] **Step 1: Scaffold Vue project**

```bash
cd /c/Users/liwenjie/Desktop/workspace/worker_helper
npm create vite@latest frontend -- --template vue
cd frontend
npm install
```

- [ ] **Step 2: Install dependencies**

```bash
cd /c/Users/liwenjie/Desktop/workspace/worker_helper/frontend
npm install vue-router@4 pinia axios
npm install -D tailwindcss @tailwindcss/vite
```

- [ ] **Step 3: Configure Vite**

Write `frontend/vite.config.js`:
```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
```

- [ ] **Step 4: Set up Tailwind**

Write `frontend/src/style.css`:
```css
@import "tailwindcss";
```

- [ ] **Step 5: Commit**

```bash
cd /c/Users/liwenjie/Desktop/workspace/worker_helper
git add frontend/
git commit -m "feat: scaffold Vue 3 + Vite + Tailwind frontend project"
```

### Task 16: Set up router, store, and API client

**Files:**
- Create: `frontend/src/router/index.js`
- Create: `frontend/src/store/index.js`
- Create: `frontend/src/api/index.js`

- [ ] **Step 1: Write router/index.js**

```javascript
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'coach', component: () => import('../views/CoachView.vue') },
  { path: '/cards', name: 'cards', component: () => import('../views/CardsView.vue') },
  { path: '/cards/:id', name: 'card-detail', component: () => import('../views/CardDetailView.vue') },
  { path: '/records', name: 'records', component: () => import('../views/RecordsView.vue') },
  { path: '/records/:id/edit', name: 'record-edit', component: () => import('../views/RecordEditView.vue') },
  { path: '/settings', name: 'settings', component: () => import('../views/SettingsView.vue') },
]

export default createRouter({ history: createWebHistory(), routes })
```

- [ ] **Step 2: Write store/index.js**

```javascript
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const showQuickNote = ref(false)
  const showReminder = ref(false)

  function toggleQuickNote() {
    showQuickNote.value = !showQuickNote.value
  }

  return { showQuickNote, showReminder, toggleQuickNote }
})
```

- [ ] **Step 3: Write api/index.js**

```javascript
import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export default {
  // Records
  createRecord(content, sourceType = 'quick_note') {
    return api.post('/records', { content, source_type: sourceType })
  },
  listRecords(params) {
    return api.get('/records', { params })
  },
  getRecord(id) {
    return api.get(`/records/${id}`)
  },
  updateRecord(id, content) {
    return api.put(`/records/${id}`, { content })
  },
  deleteRecord(id) {
    return api.delete(`/records/${id}`)
  },

  // Cards
  listCards(params) {
    return api.get('/cards', { params })
  },
  getCard(id) {
    return api.get(`/cards/${id}`)
  },
  updateCard(id, data) {
    return api.put(`/cards/${id}`, data)
  },

  // Coach
  coachChat(content) {
    return api.post('/coach/chat', { content })
  },

  // Settings
  getLLMSettings() {
    return api.get('/settings/llm')
  },
  updateLLMSettings(data) {
    return api.put('/settings/llm', data)
  },
  getReminderSettings() {
    return api.get('/settings/reminder')
  },
  updateReminderSettings(data) {
    return api.put('/settings/reminder', data)
  },
  getReminderStatus() {
    return api.get('/settings/reminder/status')
  },
}
```

- [ ] **Step 4: Update main.js**

Write `frontend/src/main.js`:
```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
```

- [ ] **Step 5: Commit**

```bash
cd /c/Users/liwenjie/Desktop/workspace/worker_helper
git add frontend/src/
git commit -m "feat: add Vue router, Pinia store, and API client"
```

---

## Phase 8: Frontend Layout & Components

### Task 17: Create App layout with sidebar navigation

**Files:**
- Create: `frontend/src/App.vue`
- Create: `frontend/src/components/AppLayout.vue`
- Create: `frontend/src/components/SideNav.vue`

- [ ] **Step 1: Write App.vue**

```vue
<template>
  <AppLayout>
    <router-view />
    <ReminderPopup v-if="store.showReminder" @close="store.showReminder = false" />
  </AppLayout>
</template>

<script setup>
import AppLayout from './components/AppLayout.vue'
import ReminderPopup from './components/ReminderPopup.vue'
import { useAppStore } from './store'
import api from './api'
import { onMounted } from 'vue'

const store = useAppStore()

// Poll reminder status every 60 seconds
onMounted(() => {
  setInterval(async () => {
    try {
      const { data } = await api.getReminderStatus()
      if (data.should_remind) store.showReminder = true
    } catch {}
  }, 60000)
})
</script>
```

- [ ] **Step 2: Write AppLayout.vue**

```vue
<template>
  <div class="flex h-screen bg-gray-950 text-gray-100">
    <SideNav @toggle-quick-note="store.toggleQuickNote()" />
    <div class="flex-1 flex flex-col overflow-hidden">
      <QuickNotePanel v-if="store.showQuickNote" @close="store.showQuickNote = false" />
      <main class="flex-1 overflow-y-auto p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import SideNav from './SideNav.vue'
import QuickNotePanel from './QuickNotePanel.vue'
import { useAppStore } from './store'

const store = useAppStore()
</script>
```

- [ ] **Step 3: Write SideNav.vue**

```vue
<template>
  <aside class="w-52 bg-gray-900 border-r border-gray-800 flex flex-col p-4">
    <h1 class="text-lg font-bold mb-8 text-purple-400">经验工厂</h1>
    <nav class="flex flex-col gap-1 flex-1">
      <router-link to="/" class="nav-item" :class="{ active: $route.name === 'coach' }">
        💬 教练对话
      </router-link>
      <router-link to="/cards" class="nav-item" :class="{ active: $route.name === 'cards' }">
        📋 经验卡片
      </router-link>
      <router-link to="/records" class="nav-item" :class="{ active: $route.name === 'records' }">
        📝 原始记录
      </router-link>
    </nav>
    <div class="border-t border-gray-800 pt-4 flex flex-col gap-2">
      <button @click="$emit('toggleQuickNote')" class="text-sm text-gray-400 hover:text-purple-400 text-left">
        ✏️ 随手记
      </button>
      <router-link to="/settings" class="nav-item text-sm" :class="{ active: $route.name === 'settings' }">
        ⚙️ 设置
      </router-link>
    </div>
  </aside>
</template>

<script setup>
defineEmits(['toggleQuickNote'])
</script>

<style scoped>
.nav-item {
  @apply px-3 py-2 rounded-lg text-gray-400 hover:bg-gray-800 hover:text-gray-200 transition-colors text-sm;
}
.nav-item.active {
  @apply bg-purple-900/40 text-purple-300;
}
</style>
```

- [ ] **Step 5: Commit**

```bash
git add frontend/src/App.vue frontend/src/components/AppLayout.vue frontend/src/components/SideNav.vue
git commit -m "feat: add main app layout with sidebar navigation"
```

### Task 18: Create QuickNotePanel and ReminderPopup components

**Files:**
- Create: `frontend/src/components/QuickNotePanel.vue`
- Create: `frontend/src/components/ReminderPopup.vue`

- [ ] **Step 1: Write QuickNotePanel.vue**

```vue
<template>
  <div class="fixed right-0 top-0 h-full w-80 bg-gray-900 border-l border-gray-800 z-50 shadow-2xl p-4">
    <div class="flex justify-between items-center mb-4">
      <h3 class="font-semibold">📝 随手记</h3>
      <button @click="$emit('close')" class="text-gray-500 hover:text-gray-300 text-lg leading-none">&times;</button>
    </div>
    <textarea
      v-model="content"
      placeholder="想到了什么？直接记..."
      class="w-full h-32 bg-gray-800 border border-gray-700 rounded-lg p-3 text-sm text-gray-200 placeholder-gray-500 resize-none focus:outline-none focus:border-purple-500"
    ></textarea>
    <button
      @click="save"
      :disabled="!content.trim() || saving"
      class="mt-3 w-full py-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 rounded-lg text-sm font-medium transition-colors"
    >
      {{ saving ? '保存中...' : '保存' }}
    </button>
    <div v-if="saved" class="mt-2 text-xs text-green-400">已保存，AI 正在加工...</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const emit = defineEmits(['close'])
const content = ref('')
const saving = ref(false)
const saved = ref(false)

async function save() {
  if (!content.value.trim()) return
  saving.value = true
  try {
    await api.createRecord(content.value, 'quick_note')
    saved.value = true
    setTimeout(() => { content.value = ''; saved.value = false; emit('close') }, 1500)
  } catch (e) {
    alert('保存失败: ' + e.message)
  } finally {
    saving.value = false
  }
}
</script>
```

- [ ] **Step 2: Write ReminderPopup.vue**

```vue
<template>
  <div class="fixed bottom-6 right-6 w-96 bg-gray-900 border border-gray-700 rounded-xl shadow-2xl z-50 overflow-hidden">
    <div class="bg-purple-900/60 px-4 py-2 flex justify-between items-center">
      <span class="text-sm font-medium">⏰ 经验教练 · 每日快问</span>
      <button @click="$emit('close')" class="text-gray-400 hover:text-gray-200">&times;</button>
    </div>
    <div class="p-4 space-y-3">
      <div v-for="(msg, i) in messages" :key="i" class="flex gap-2" :class="msg.role === 'user' ? 'justify-end' : ''">
        <div v-if="msg.role === 'coach'" class="w-6 h-6 rounded-full bg-teal-500 flex items-center justify-center text-xs flex-shrink-0">AI</div>
        <div class="rounded-lg px-3 py-2 text-sm max-w-[80%]" :class="msg.role === 'coach' ? 'bg-gray-800' : 'bg-purple-900/40'">
          {{ msg.content }}
        </div>
        <div v-if="msg.role === 'user'" class="w-6 h-6 rounded-full bg-yellow-500 flex items-center justify-center text-xs flex-shrink-0">我</div>
      </div>
    </div>
    <div class="border-t border-gray-800 p-3 flex gap-2">
      <input
        v-model="input"
        @keyup.enter="send"
        placeholder="输入回复..."
        class="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-purple-500"
      />
      <button @click="send" class="px-4 py-2 bg-teal-500 hover:bg-teal-600 rounded-lg text-sm font-medium text-black">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const emit = defineEmits(['close'])
const input = ref('')
const messages = ref([{ role: 'coach', content: '今天主要做了什么？一句话就行 👋' }])

async function send() {
  if (!input.value.trim()) return
  const userMsg = input.value
  messages.value.push({ role: 'user', content: userMsg })
  input.value = ''
  try {
    const { data } = await api.coachChat(userMsg)
    messages.value.push({ role: 'coach', content: data.response })
  } catch {
    messages.value.push({ role: 'coach', content: '抱歉，出错了。请稍后再试。' })
  }
}
</script>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/QuickNotePanel.vue frontend/src/components/ReminderPopup.vue
git commit -m "feat: add quick note panel and reminder popup components"
```

### Task 19: Create Coach chat view

**Files:**
- Create: `frontend/src/views/CoachView.vue`
- Create: `frontend/src/components/CoachChat.vue`

- [ ] **Step 1: Write CoachChat.vue**

```vue
<template>
  <div class="max-w-3xl mx-auto flex flex-col h-[calc(100vh-8rem)]">
    <div class="mb-4">
      <h2 class="text-xl font-bold">💬 教练对话</h2>
      <p class="text-gray-500 text-sm mt-1">AI 教练会引导你回顾工作，你只需要自然回答</p>
    </div>
    <div class="flex-1 overflow-y-auto space-y-3 mb-4" ref="chatContainer">
      <div v-for="(msg, i) in messages" :key="i" class="flex gap-3" :class="msg.role === 'user' ? 'justify-end' : ''">
        <div v-if="msg.role === 'coach'" class="w-8 h-8 rounded-full bg-teal-500 flex items-center justify-center text-sm flex-shrink-0">AI</div>
        <div class="rounded-lg px-4 py-2.5 max-w-[75%]" :class="msg.role === 'coach' ? 'bg-gray-800 text-gray-200' : 'bg-purple-900/40 text-gray-100'">
          {{ msg.content }}
        </div>
        <div v-if="msg.role === 'user'" class="w-8 h-8 rounded-full bg-yellow-500 flex items-center justify-center text-sm flex-shrink-0">我</div>
      </div>
      <div v-if="loading" class="flex gap-3">
        <div class="w-8 h-8 rounded-full bg-teal-500 flex items-center justify-center text-sm">AI</div>
        <div class="bg-gray-800 rounded-lg px-4 py-2.5 text-gray-400">思考中...</div>
      </div>
    </div>
    <div class="flex gap-2">
      <input
        v-model="input"
        @keyup.enter="send"
        :disabled="loading"
        placeholder="描述你今天的工作..."
        class="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-gray-200 placeholder-gray-500 focus:outline-none focus:border-purple-500"
      />
      <button @click="send" :disabled="loading || !input.trim()" class="px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 rounded-lg font-medium transition-colors">
        发送
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import api from '../api'

const input = ref('')
const messages = ref([{ role: 'coach', content: '你好！我是你的经验教练 🎯 今天做了什么工作？简单说说就行~' }])
const loading = ref(false)
const chatContainer = ref(null)

async function send() {
  if (!input.value.trim() || loading.value) return
  const userMsg = input.value
  messages.value.push({ role: 'user', content: userMsg })
  input.value = ''
  loading.value = true
  await nextTick()
  scrollBottom()
  try {
    const { data } = await api.coachChat(userMsg)
    messages.value.push({ role: 'coach', content: data.response })
  } catch {
    messages.value.push({ role: 'coach', content: '抱歉，出了点问题。请稍后再试。' })
  } finally {
    loading.value = false
    await nextTick()
    scrollBottom()
  }
}

function scrollBottom() {
  if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight
}
</script>
```

- [ ] **Step 2: Write CoachView.vue**

```vue
<template>
  <CoachChat />
</template>

<script setup>
import CoachChat from '../components/CoachChat.vue'
</script>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/CoachChat.vue frontend/src/views/CoachView.vue
git commit -m "feat: add coach chat view with conversational AI interface"
```

### Task 20: Create experience cards views

**Files:**
- Create: `frontend/src/views/CardsView.vue`
- Create: `frontend/src/components/CardList.vue`
- Create: `frontend/src/views/CardDetailView.vue`
- Create: `frontend/src/components/CardDetail.vue`

- [ ] **Step 1: Write CardList.vue**

```vue
<template>
  <div>
    <div class="flex gap-3 mb-6 flex-wrap">
      <input
        v-model="search"
        @input="fetch"
        placeholder="搜索卡片..."
        class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-purple-500 w-64"
      />
      <select v-model="skillTag" @change="fetch" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200">
        <option value="">全部技能</option>
        <option v-for="tag in allTags" :key="tag" :value="tag">{{ tag }}</option>
      </select>
    </div>
    <div v-if="cards.length === 0" class="text-gray-500 text-center py-12">
      还没有经验卡片。去和教练聊聊，或者记点东西吧~
    </div>
    <div class="grid gap-4 md:grid-cols-2">
      <div
        v-for="card in cards" :key="card.id"
        @click="$router.push(`/cards/${card.id}`)"
        class="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-purple-700/50 cursor-pointer transition-colors"
      >
        <div class="flex justify-between items-start mb-3">
          <h3 class="font-semibold text-gray-100">{{ card.title }}</h3>
          <span class="text-xs px-2 py-1 rounded-full" :class="scoreColor(card.quality_score)">
            {{ card.quality_score }}
          </span>
        </div>
        <p class="text-sm text-gray-400 line-clamp-2 mb-3">{{ card.tech_solution }}</p>
        <div class="flex flex-wrap gap-1.5">
          <span v-for="tag in card.skill_tags" :key="tag" class="text-xs bg-gray-800 text-teal-400 px-2 py-0.5 rounded">
            {{ tag }}
          </span>
        </div>
        <div class="text-xs text-gray-600 mt-3">{{ formatDate(card.created_at) }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const cards = ref([])
const search = ref('')
const skillTag = ref('')
const allTags = ref([])

function scoreColor(s) {
  if (s >= 80) return 'bg-green-900/60 text-green-400'
  if (s >= 60) return 'bg-yellow-900/60 text-yellow-400'
  return 'bg-red-900/60 text-red-400'
}

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN')
}

async function fetch() {
  const { data } = await api.listCards({ search: search.value, skill_tag: skillTag.value || undefined })
  cards.value = data
  allTags.value = [...new Set(data.flatMap(c => c.skill_tags))]
}

onMounted(fetch)
</script>
```

- [ ] **Step 2: Write CardsView.vue**

```vue
<template>
  <div>
    <h2 class="text-xl font-bold mb-6">📋 经验卡片</h2>
    <CardList />
  </div>
</template>

<script setup>
import CardList from '../components/CardList.vue'
</script>
```

- [ ] **Step 3: Write CardDetail.vue**

```vue
<template>
  <div class="max-w-3xl mx-auto">
    <button @click="$router.back()" class="text-gray-400 hover:text-gray-200 mb-4 inline-block">&larr; 返回</button>

    <div v-if="card" class="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <div class="flex justify-between items-start mb-6">
        <h2 class="text-xl font-bold">{{ card.title }}</h2>
        <span class="text-sm px-3 py-1 rounded-full bg-green-900/60 text-green-400">{{ card.quality_score }} 分</span>
      </div>

      <div class="space-y-4">
        <div>
          <label class="text-xs text-gray-500 uppercase">背景</label>
          <p class="text-gray-200 mt-1">{{ card.background }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase">技术方案</label>
          <p class="text-gray-200 mt-1">{{ card.tech_solution }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase">量化成果</label>
          <p class="text-teal-400 mt-1 font-medium">{{ card.quantifiable_result }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase">反思</label>
          <p class="text-gray-200 mt-1">{{ card.reflection || '暂无' }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase">技能标签</label>
          <div class="flex flex-wrap gap-1.5 mt-1">
            <span v-for="tag in card.skill_tags" :key="tag" class="text-xs bg-gray-800 text-teal-400 px-2 py-0.5 rounded">{{ tag }}</span>
          </div>
        </div>
      </div>

      <div class="mt-6 pt-4 border-t border-gray-800 flex gap-3">
        <router-link v-if="card.source_record_id" :to="`/records/${card.source_record_id}/edit`" class="text-sm text-purple-400 hover:text-purple-300">
          查看原始记录 &rarr;
        </router-link>
        <span class="text-xs text-gray-600">{{ formatDate(card.created_at) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()
const card = ref(null)

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN')
}

onMounted(async () => {
  const { data } = await api.getCard(route.params.id)
  card.value = data
})
</script>
```

- [ ] **Step 4: Write CardDetailView.vue**

```vue
<template>
  <CardDetail />
</template>

<script setup>
import CardDetail from '../components/CardDetail.vue'
</script>
```

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/CardsView.vue frontend/src/views/CardDetailView.vue frontend/src/components/CardList.vue frontend/src/components/CardDetail.vue
git commit -m "feat: add experience card list and detail views"
```

### Task 21: Create raw records views

**Files:**
- Create: `frontend/src/views/RecordsView.vue`
- Create: `frontend/src/components/RecordList.vue`
- Create: `frontend/src/views/RecordEditView.vue`

- [ ] **Step 1: Write RecordList.vue**

```vue
<template>
  <div>
    <div class="flex gap-3 mb-6">
      <select v-model="sourceType" @change="fetch" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200">
        <option value="">全部来源</option>
        <option value="chat">教练对话</option>
        <option value="quick_note">随手记</option>
      </select>
      <select v-model="processStatus" @change="fetch" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200">
        <option value="">全部状态</option>
        <option value="pending">待加工</option>
        <option value="processed">已加工</option>
      </select>
    </div>
    <div v-if="records.length === 0" class="text-gray-500 text-center py-12">
      还没有原始记录。
    </div>
    <div class="space-y-3">
      <div
        v-for="record in records" :key="record.id"
        class="bg-gray-900 border border-gray-800 rounded-lg p-4 hover:border-gray-700 transition-colors"
      >
        <div class="flex justify-between items-start mb-2">
          <div class="flex gap-2 items-center">
            <span class="text-xs px-2 py-0.5 rounded" :class="record.source_type === 'chat' ? 'bg-blue-900/60 text-blue-400' : 'bg-purple-900/60 text-purple-400'">
              {{ record.source_type === 'chat' ? '对话' : '快记' }}
            </span>
            <span class="text-xs px-2 py-0.5 rounded" :class="record.process_status === 'processed' ? 'bg-green-900/60 text-green-400' : 'bg-yellow-900/60 text-yellow-400'">
              {{ record.process_status === 'processed' ? '已加工' : '待加工' }}
            </span>
          </div>
          <span class="text-xs text-gray-600">{{ formatDate(record.recorded_at) }}</span>
        </div>
        <p class="text-sm text-gray-300 line-clamp-2">{{ record.content }}</p>
        <div class="mt-3">
          <router-link :to="`/records/${record.id}/edit`" class="text-xs text-purple-400 hover:text-purple-300">编辑</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const records = ref([])
const sourceType = ref('')
const processStatus = ref('')

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN')
}

async function fetch() {
  const params = {}
  if (sourceType.value) params.source_type = sourceType.value
  if (processStatus.value) params.process_status = processStatus.value
  const { data } = await api.listRecords(params)
  records.value = data
}

onMounted(fetch)
</script>
```

- [ ] **Step 2: Write RecordsView.vue**

```vue
<template>
  <div>
    <h2 class="text-xl font-bold mb-6">📝 原始记录</h2>
    <RecordList />
  </div>
</template>

<script setup>
import RecordList from '../components/RecordList.vue'
</script>
```

- [ ] **Step 3: Write RecordEditView.vue**

```vue
<template>
  <div class="max-w-3xl mx-auto">
    <button @click="$router.back()" class="text-gray-400 hover:text-gray-200 mb-4 inline-block">&larr; 返回</button>
    <h2 class="text-xl font-bold mb-6">✏️ 编辑原始记录</h2>
    <div v-if="record" class="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <div class="mb-4">
        <label class="text-xs text-gray-500 uppercase mb-2 block">原始内容</label>
        <textarea
          v-model="content"
          class="w-full h-48 bg-gray-800 border border-gray-700 rounded-lg p-4 text-gray-200 focus:outline-none focus:border-purple-500 resize-none"
        ></textarea>
      </div>
      <div class="flex gap-3">
        <button @click="save" :disabled="saving" class="px-6 py-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 rounded-lg font-medium transition-colors">
          {{ saving ? '保存中...' : '保存并重新加工' }}
        </button>
        <button @click="$router.back()" class="px-6 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg font-medium transition-colors">
          取消
        </button>
      </div>
      <div v-if="saved" class="mt-3 text-sm text-green-400">已保存，AI 正在重新加工经验卡片...</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()
const record = ref(null)
const content = ref('')
const saving = ref(false)
const saved = ref(false)

onMounted(async () => {
  const { data } = await api.getRecord(route.params.id)
  record.value = data
  content.value = data.content
})

async function save() {
  saving.value = true
  try {
    await api.updateRecord(route.params.id, content.value)
    saved.value = true
    setTimeout(() => { saved.value = false }, 3000)
  } catch (e) {
    alert('保存失败: ' + e.message)
  } finally {
    saving.value = false
  }
}
</script>
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/RecordsView.vue frontend/src/views/RecordEditView.vue frontend/src/components/RecordList.vue
git commit -m "feat: add raw record list and edit views with re-processing"
```

### Task 22: Create settings view

**Files:**
- Create: `frontend/src/views/SettingsView.vue`
- Create: `frontend/src/components/SettingsPanel.vue`

- [ ] **Step 1: Write SettingsPanel.vue**

```vue
<template>
  <div class="max-w-2xl space-y-8">
    <!-- LLM Settings -->
    <section class="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <h3 class="font-semibold mb-4">🤖 LLM 配置</h3>
      <div class="space-y-4">
        <div>
          <label class="text-sm text-gray-400 block mb-1">模型供应商</label>
          <select v-model="llm.llm_provider" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200">
            <option value="claude">Claude (Anthropic)</option>
            <option value="openai">OpenAI (GPT)</option>
          </select>
        </div>
        <div>
          <label class="text-sm text-gray-400 block mb-1">API Key</label>
          <input v-model="llm.llm_api_key" type="password" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200" />
        </div>
        <div>
          <label class="text-sm text-gray-400 block mb-1">Base URL (可选)</label>
          <input v-model="llm.llm_base_url" placeholder="留空使用默认" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200" />
        </div>
        <div>
          <label class="text-sm text-gray-400 block mb-1">模型名称</label>
          <input v-model="llm.llm_model" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200" />
        </div>
        <button @click="saveLLM" :disabled="savingLLM" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 rounded-lg text-sm font-medium">
          {{ savingLLM ? '保存中...' : '保存 LLM 配置' }}
        </button>
        <div v-if="llmSaved" class="text-sm text-green-400">配置已保存，LLM 提供者已重置</div>
      </div>
    </section>

    <!-- Reminder Settings -->
    <section class="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <h3 class="font-semibold mb-4">⏰ 提醒设置</h3>
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <input v-model="reminder.reminder_enabled" type="checkbox" class="w-4 h-4" />
          <label class="text-sm text-gray-300">启用每日提醒</label>
        </div>
        <div>
          <label class="text-sm text-gray-400 block mb-1">提醒时间</label>
          <input v-model="reminder.reminder_time" type="time" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200" />
        </div>
        <button @click="saveReminder" :disabled="savingReminder" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 rounded-lg text-sm font-medium">
          {{ savingReminder ? '保存中...' : '保存提醒配置' }}
        </button>
        <div v-if="reminderSaved" class="text-sm text-green-400">配置已保存</div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../api'

const llm = reactive({ llm_provider: 'claude', llm_api_key: '', llm_base_url: '', llm_model: 'claude-sonnet-4-6' })
const reminder = reactive({ reminder_enabled: true, reminder_time: '17:30' })
const savingLLM = ref(false)
const savingReminder = ref(false)
const llmSaved = ref(false)
const reminderSaved = ref(false)

onMounted(async () => {
  try {
    const { data: d } = await api.getLLMSettings()
    Object.assign(llm, d)
  } catch {}
  try {
    const { data: d } = await api.getReminderSettings()
    Object.assign(reminder, d)
  } catch {}
})

async function saveLLM() {
  savingLLM.value = true
  try {
    await api.updateLLMSettings({ ...llm })
    llmSaved.value = true
    setTimeout(() => llmSaved.value = false, 3000)
  } catch (e) {
    alert('保存失败: ' + e.message)
  } finally {
    savingLLM.value = false
  }
}

async function saveReminder() {
  savingReminder.value = true
  try {
    await api.updateReminderSettings({ ...reminder })
    reminderSaved.value = true
    setTimeout(() => reminderSaved.value = false, 3000)
  } catch (e) {
    alert('保存失败: ' + e.message)
  } finally {
    savingReminder.value = false
  }
}
</script>
```

- [ ] **Step 2: Write SettingsView.vue**

```vue
<template>
  <div>
    <h2 class="text-xl font-bold mb-6">⚙️ 设置</h2>
    <SettingsPanel />
  </div>
</template>

<script setup>
import SettingsPanel from '../components/SettingsPanel.vue'
</script>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/SettingsView.vue frontend/src/components/SettingsPanel.vue
git commit -m "feat: add settings view for LLM and reminder configuration"
```

---

## Phase 9: Integration & Final Verification

### Task 23: Run full backend test suite

- [ ] **Step 1: Run all backend tests**

```bash
cd /c/Users/liwenjie/Desktop/workspace/worker_helper
source .venv/Scripts/activate
python -m pytest backend/tests/ -v
# Expected: all tests pass
```

### Task 24: Verify frontend builds

- [ ] **Step 1: Build frontend**

```bash
cd /c/Users/liwenjie/Desktop/workspace/worker_helper/frontend
npm run build
# Expected: build succeeds with no errors
```

### Task 25: Create .env.example

**Files:**
- Create: `.env.example`

- [ ] **Step 1: Write .env.example**

```
LLM_PROVIDER=claude
LLM_API_KEY=your-api-key-here
LLM_BASE_URL=
LLM_MODEL=claude-sonnet-4-6
REMINDER_ENABLED=true
REMINDER_TIME=17:30
DATABASE_URL=sqlite:///experience_factory.db
```

- [ ] **Step 2: Final commit**

```bash
git add .env.example
git commit -m "chore: add env example file and finalize MVP"
```

- [ ] **Step 3: Final test run**

```bash
python -m pytest backend/tests/ -v
# Expected: all green
```
