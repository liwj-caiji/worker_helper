import threading

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal, get_db
from backend.models import RawRecord, SourceType
from backend.schemas import CoachMessage
from backend.services.coach import get_coach_response
from backend.services.pipeline import process_record

router = APIRouter(prefix="/api/coach", tags=["coach"])


def _process_async(record_id: int):
    db = SessionLocal()
    try:
        record = db.query(RawRecord).filter(RawRecord.id == record_id).first()
        if record and record.process_status != "processed":
            process_record(db, record)
    finally:
        db.close()


@router.post("/chat")
def coach_chat(message: CoachMessage, db: Session = Depends(get_db)):
    record = RawRecord(content=message.content, source_type=SourceType.chat)
    db.add(record)
    db.commit()
    db.refresh(record)

    if len(message.content.strip()) > 10:
        threading.Thread(target=_process_async, args=(record.id,), daemon=True).start()

    history = [{"role": h.role, "content": h.content} for h in message.history]
    response = get_coach_response(message.content, conversation_history=history)
    return {"response": response, "record_id": record.id}
