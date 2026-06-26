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


@pytest.fixture
def mock_pipeline():
    """管道 mock：返回合法提取结果和评分，后台线程不报错"""
    mock = MagicMock()
    mock.chat.side_effect = [
        '{"title":"测试","background":"bg","tech_solution":"tech","quantifiable_result":"result","reflection":"","skill_tags":["Tag1"]}',
        "70",
    ]
    return mock


def test_coach_chat(client, mock_pipeline):
    mock_coach = MagicMock()
    mock_coach.chat.return_value = "听起来你今天做了很有价值的工作！能告诉我具体用到了什么技术吗？"

    with patch("backend.services.pipeline.get_provider", return_value=mock_pipeline), \
         patch("backend.services.coach.get_provider", return_value=mock_coach):
        resp = client.post("/api/coach/chat", json={"content": "今天优化了数据库查询性能，速度提升明显"})
    assert resp.status_code == 200
    data = resp.json()
    assert "response" in data
    assert "record_id" in data
    assert "技术" in data["response"]


def test_coach_short_message_skips_pipeline(client, mock_pipeline):
    """消息不超过10字符时跳过管道加工"""
    mock_coach = MagicMock()
    mock_coach.chat.return_value = "你好！"

    with patch("backend.services.pipeline.get_provider", return_value=mock_pipeline), \
         patch("backend.services.coach.get_provider", return_value=mock_coach):
        resp = client.post("/api/coach/chat", json={"content": "你好"})
    assert resp.status_code == 200
    assert "response" in resp.json()
