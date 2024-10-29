from sqlalchemy import Column, Integer, String

from .database import Base


class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    gender = Column(String)
    avatar = Column(String)  # путь к аватарке
