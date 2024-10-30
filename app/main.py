from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import Participant
from .schemas import ParticipantCreate
from .services import check_daily_like_limit, save_avatar_with_watermark

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


@app.post("/api/clients/{id}/match")
def match_participant(
    id: int, current_user_id: int, db: Session = Depends(get_db)
):
    participant = db.query(Participant).get(id)
    current_user = db.query(Participant).get(current_user_id)
    if not participant or not current_user:
        raise HTTPException(status_code=404, detail="Участник не найден")

    # Проверка лимита лайков у текущего пользователя
    check_daily_like_limit(current_user, db)

    # Проверка на взаимную симпатию
    if participant.mutual_like_id == current_user.id:
        return {
            "message": (
                f"Вы понравились {participant.first_name}! "
                f"Почта участника: {participant.email}. "
                "Уведомление будет отправлено."
            )
        }
    else:
        # Если симпатии нет, сохраняем
        current_user.mutual_like_id = id
        db.commit()
        return {"message": "Оценка участника сохранена."}
