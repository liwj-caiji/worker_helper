from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import RawRecord, SourceType
from backend.schemas import CoachMessage
from backend.services.coach import get_coach_response
from backend.services.pipeline import process_record

router = APIRouter(prefix="/api/coach", tags=["coach"])


@router.post("/chat")
def coach_chat(message: CoachMessage, db: Session = Depends(get_db)):
    record = RawRecord(content=message.content, source_type=SourceType.chat)
    db.add(record)
    db.commit()
    db.refresh(record)

    if len(message.content.strip()) > 10:
        process_record(db, record)
        db.refresh(record)

    response = get_coach_response(message.content)
    return {"response": response, "record_id": record.id}
