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
