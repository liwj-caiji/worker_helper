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
