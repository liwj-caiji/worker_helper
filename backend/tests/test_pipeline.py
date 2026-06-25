import itertools
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
    mock.chat.side_effect = itertools.cycle([
        '{"title":"查询性能优化","background":"Q2 交易系统后端","tech_solution":"Redis缓存热点查询","quantifiable_result":"查询耗时 2.3s -> 180ms","reflection":"要注意缓存穿透","skill_tags":["Redis","性能优化"]}',
        "85",
    ])
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
