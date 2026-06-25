from fastapi import APIRouter, Depends, HTTPException
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
