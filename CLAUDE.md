# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all backend tests
uv run python -m pytest backend/tests/ -v

# Run a single test file
uv run python -m pytest backend/tests/test_models.py -v

# Run a specific test
uv run python -m pytest backend/tests/test_pipeline.py::test_process_record_creates_card -v

# Start backend dev server (port 8000)
uv run uvicorn backend.main:app --reload

# Start frontend dev server (port 5173, proxies /api → :8000)
cd frontend && npm run dev

# Build frontend for production
cd frontend && npm run build
```

## Architecture

### Core data flow

```
User input (coach chat / quick note)
    → RawRecord (saved in raw_records table)
    → process_record() pipeline (AI: extract → score → tag)
    → ExperienceCard upserted (experience_cards table, linked via source_record_id)
    → SkillNodes created/updated
```

When a user edits a RawRecord, `process_record()` is called again — it upserts the linked ExperienceCard (same card, updated fields) rather than creating a duplicate.

### LLM Provider abstraction (`backend/llm/`)

`LLMProvider` is an ABC with a single `chat(system_prompt, user_message) -> str` method. The singleton factory (`get_provider()`) reads `settings.llm_provider` and instantiates the matching implementation. Changing the LLM requires only updating the `.env` config or settings API — no pipeline code changes.

### Config

`backend/config.py` uses `pydantic-settings`, reading from `.env` automatically. `llm_api_key` is typed as `SecretStr` — call `.get_secret_value()` to extract the actual key (see `factory.py:23`).

### Database

SQLite via SQLAlchemy, with `check_same_thread=False` for FastAPI compatibility. `Base.metadata.create_all()` runs on startup. Tests recreate tables per-function via the `conftest.py` fixture (drop → create → yield → drop).

### API endpoints

| Prefix | File | Purpose |
|---|---|---|
| `/api/records` | `routers/records.py` | RawRecord CRUD; create/update triggers pipeline |
| `/api/cards` | `routers/cards.py` | ExperienceCard list (search/filter) + detail + update |
| `/api/coach` | `routers/coach.py` | POST `/chat` — saves record, runs pipeline, returns AI response |
| `/api/settings` | `routers/settings.py` | LLM config (GET/PUT), reminder config, reminder status poll |

### Frontend

Vue 3 SPA with Vite dev proxy (`/api` → `localhost:8000`). Pinia store (`useAppStore`) manages `showQuickNote` and `showReminder` state. The `App.vue` polls `/api/settings/reminder/status` every 60s for the reminder popup trigger.

### Key schema detail

`ExperienceCardOut.metadata_` uses `serialization_alias="metadata"` (not `alias`) because SQLAlchemy's Base already has a `metadata` attribute. The column is named `metadata_` in Python but stores as `"metadata"` in DB and JSON.
