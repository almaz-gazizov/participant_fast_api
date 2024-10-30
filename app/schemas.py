from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ParticipantCreate(BaseModel):
    name: str
    surname: str
    email: str
    gender: str
    avatar: str
    password: str
    latitude: float
    longitude: float


class ParticipantFilter(BaseModel):
    gender: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    max_distance: Optional[float] = None


class ParticipantResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    gender: str
    avatar: Optional[str] = None
    likes: int
    registration_date: datetime
    latitude: float
    longitude: float

    class Config:
        from_attributes = True
