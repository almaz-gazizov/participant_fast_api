from typing import Optional

from pydantic import BaseModel


class ParticipantCreate(BaseModel):
    name: str
    surname: str
    email: str
    gender: str
    avatar: str
    password: str


class ParticipantFilter(BaseModel):
    gender: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
