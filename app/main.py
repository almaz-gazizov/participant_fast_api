from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import Participant
from .schemas import ParticipantCreate
from .services import save_avatar_with_watermark

app = FastAPI()


@app.post("/api/clients/create")
async def create_participant(
    participant: ParticipantCreate,
    avatar: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Сохраняем аватарку с водяным знаком
    try:
        avatar_path = await save_avatar_with_watermark(avatar)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Не удалось сохранить аватар"
        )

    # Создаём объект участника с сохранённым путём к аватарке
    db_participant = Participant(
        email=participant.email,
        name=participant.name,
        surname=participant.surname,
        avatar_path=avatar_path,
        gender=participant.gender
    )

    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)

    return db_participant
