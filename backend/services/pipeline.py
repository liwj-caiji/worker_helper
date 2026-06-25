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
