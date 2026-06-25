import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import Base, engine
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
