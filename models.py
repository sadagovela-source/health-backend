from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import uuid
from datetime import datetime, timezone

def new_id():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=new_id)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    health_records = relationship("HealthRecord", back_populates="user")

class HealthRecord(Base):
    __tablename__ = "health_records"
    id = Column(String, primary_key=True, default=new_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    steps = Column(Integer, default=0)
    heart_rate = Column(Float, default=0)
    heart_rate_min = Column(Float, default=0)
    heart_rate_max = Column(Float, default=0)
    hrv = Column(Float, default=0)
    oxygen_saturation = Column(Float, default=0)
    sleep_hours = Column(Float, default=0)
    active_calories = Column(Float, default=0)
    total_calories = Column(Float, default=0)
    distance = Column(Float, default=0)
    weight = Column(Float, default=0)
    bmi = Column(Float, default=0)
    systolic_bp = Column(Float, default=0)
    diastolic_bp = Column(Float, default=0)
    blood_glucose = Column(Float, default=0)
    body_temperature = Column(Float, default=0)
    respiratory_rate = Column(Float, default=0)
    water_intake = Column(Float, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", back_populates="health_records")
