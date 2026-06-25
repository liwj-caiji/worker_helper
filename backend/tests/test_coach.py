import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import Base, engine


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
        "听起来你今天做了很有价值的工作！能告诉我具体用到了什么技术吗？",
    ]
    return mock


def test_coach_chat(client):
    fake = fake_provider()
    with patch("backend.services.pipeline.get_provider", return_value=fake), \
         patch("backend.services.coach.get_provider", return_value=fake):
        resp = client.post("/api/coach/chat", json={"content": "今天优化了数据库查询性能，速度提升明显"})
    assert resp.status_code == 200
    data = resp.json()
    assert "response" in data
    assert "record_id" in data
    assert "技术" in data["response"]
