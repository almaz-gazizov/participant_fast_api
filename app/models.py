from datetime import datetime, timezone

from sqlalchemy import (
    Column, Date, DateTime, ForeignKey, Integer, String
)

from .database import Base


class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    gender = Column(String)
    avatar = Column(String)
    likes = Column(Integer, default=0)
    mutual_like_id = Column(
        Integer, ForeignKey("participants.id"), nullable=True
    )
    last_like_date = Column(Date, default=None)
    daily_likes_count = Column(Integer, default=0)
    registration_date = Column(
        DateTime, default=datetime.now(timezone.utc)
    )
