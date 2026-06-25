from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import RawRecord
from backend.schemas import RawRecordCreate, RawRecordUpdate, RawRecordOut
from backend.services.pipeline import process_record

router = APIRouter(prefix="/api/records", tags=["records"])


@router.post("", response_model=RawRecordOut, status_code=201)
def create_record(data: RawRecordCreate, db: Session = Depends(get_db)):
    record = RawRecord(content=data.content, source_type=data.source_type)
    db.add(record)
    db.commit()
    db.refresh(record)
    if record.content.strip():
        process_record(db, record)
        db.refresh(record)
    return record


@router.get("", response_model=List[RawRecordOut])
def list_records(
    source_type: str | None = None,
    process_status: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(RawRecord)
    if source_type:
        q = q.filter(RawRecord.source_type == source_type)
    if process_status:
        q = q.filter(RawRecord.process_status == process_status)
    return q.order_by(RawRecord.recorded_at.desc()).all()


@router.get("/{record_id}", response_model=RawRecordOut)
def get_record(record_id: str, db: Session = Depends(get_db)):
    record = db.query(RawRecord).filter(RawRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@router.put("/{record_id}", response_model=RawRecordOut)
def update_record(record_id: str, data: RawRecordUpdate, db: Session = Depends(get_db)):
    record = db.query(RawRecord).filter(RawRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    record.content = data.content
    db.commit()
    db.refresh(record)
    process_record(db, record)
    db.refresh(record)
    return record


@router.delete("/{record_id}", status_code=204)
def delete_record(record_id: str, db: Session = Depends(get_db)):
    record = db.query(RawRecord).filter(RawRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(record)
    db.commit()
    return None
