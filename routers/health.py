from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from database import get_db
from models import HealthRecord
from schemas import HealthSync, HealthRecordResponse
from routers.auth import get_current_user
from models import User
from typing import List

router = APIRouter()

@router.post("/sync", status_code=201)
def sync_health(
    data: HealthSync,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    date_only = data.date.replace(hour=0, minute=0, second=0, microsecond=0,
                                   tzinfo=timezone.utc)
    record = db.query(HealthRecord).filter(
        HealthRecord.user_id == current_user.id,
        HealthRecord.date == date_only
    ).first()

    data_dict = data.dict(exclude={"date"})

    if record:
        for field, value in data_dict.items():
            setattr(record, field, value)
    else:
        record = HealthRecord(
            user_id=current_user.id,
            date=date_only,
            **data_dict
        )
        db.add(record)

    db.commit()
    db.refresh(record)
    return {"message": "Datos sincronizados correctamente", "id": record.id}

@router.get("/history", response_model=List[dict])
def get_history(
    metric: str = Query("steps"),
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    records = (
        db.query(HealthRecord)
        .filter(HealthRecord.user_id == current_user.id)
        .order_by(HealthRecord.date.desc())
        .limit(days)
        .all()
    )

    metric_map = {
        "steps": "steps", "heart": "heart_rate", "oxygen": "oxygen_saturation",
        "sleep": "sleep_hours", "calories": "active_calories", "weight": "weight",
        "glucose": "blood_glucose", "pressure": "systolic_bp",
    }
    field = metric_map.get(metric, "steps")

    return [
        {"value": getattr(r, field, 0), "date": r.date.isoformat()}
        for r in reversed(records)
    ]

@router.get("/today")
def get_today(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0)
    record = db.query(HealthRecord).filter(
        HealthRecord.user_id == current_user.id,
        HealthRecord.date == today
    ).first()
    if not record:
        return {}
    return {c.name: getattr(record, c.name)
            for c in HealthRecord.__table__.columns}

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    records = db.query(HealthRecord).filter(
        HealthRecord.user_id == current_user.id
    ).order_by(HealthRecord.date.desc()).limit(30).all()

    if not records:
        return {"message": "Sin datos"}

    avg_steps = sum(r.steps for r in records) / len(records)
    avg_hr = sum(r.heart_rate for r in records if r.heart_rate > 0)
    avg_sleep = sum(r.sleep_hours for r in records if r.sleep_hours > 0)

    return {
        "total_records": len(records),
        "avg_steps_30d": round(avg_steps),
        "avg_heart_rate_30d": round(avg_hr / len(records), 1),
        "avg_sleep_30d": round(avg_sleep / len(records), 1),
        "last_weight": records[0].weight if records else 0,
    }
