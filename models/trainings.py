from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, EmailStr


class Training(Document):
    """Групповое занятие фитнес-клуба (коллекция trainings)."""
    title: str
    trainer: str
    hall: str
    start_time: datetime
    capacity: int
    description: str = ""
    enrolled: List[EmailStr] = []

    class Settings:
        name = "trainings"

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Утренняя йога",
                "trainer": "Иванова А.",
                "hall": "Зал 2",
                "start_time": "2026-11-05T08:00:00",
                "capacity": 15,
                "description": "Занятие для начинающих",
                "enrolled": [],
            }
        }
    }


class TrainingUpdate(BaseModel):
    title: Optional[str] = None
    trainer: Optional[str] = None
    hall: Optional[str] = None
    start_time: Optional[datetime] = None
    capacity: Optional[int] = None
    description: Optional[str] = None


class EnrollRequest(BaseModel):
    email: EmailStr
