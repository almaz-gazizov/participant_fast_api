from pydantic import BaseModel


class ParticipantCreate(BaseModel):
    name: str
    surname: str
    email: str
    gender: str
    avatar: str
    password: str
