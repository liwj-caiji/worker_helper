import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
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
