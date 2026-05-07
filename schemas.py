from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    token: str

class HealthSync(BaseModel):
    date: datetime
    steps: int = 0
    heart_rate: float = 0
    heart_rate_min: float = 0
    heart_rate_max: float = 0
    hrv: float = 0
    oxygen_saturation: float = 0
    sleep_hours: float = 0
    active_calories: float = 0
    total_calories: float = 0
    distance: float = 0
    weight: float = 0
    bmi: float = 0
    systolic_bp: float = 0
    diastolic_bp: float = 0
    blood_glucose: float = 0
    body_temperature: float = 0
    respiratory_rate: float = 0
    water_intake: float = 0

class HealthRecordResponse(BaseModel):
    id: str
    date: datetime
    steps: int
    heart_rate: float
    oxygen_saturation: float
    sleep_hours: float
    active_calories: float
    weight: float
    systolic_bp: float
    diastolic_bp: float
    blood_glucose: float

    class Config:
        orm_mode = True
