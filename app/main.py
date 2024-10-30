from functools import lru_cache
from typing import List

from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from .auth import get_current_user
from .database import get_db
from .models import Participant
from .schemas import ParticipantCreate, ParticipantFilter
from .services import (
    calculate_distance, check_daily_like_limit, save_avatar_with_watermark
)

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


def get_current_user_id(
    db: Session = Depends(get_db), token: str = Depends(get_current_user)
):
    user = db.query(Participant).filter(
        Participant.id == token.user_id
    ).first()
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user.id


@lru_cache(maxsize=128)
def get_cached_participants(
    gender: str, name: str, surname: str, current_location: tuple,
    max_distance: float, db_session: Session
):
    query = db_session.query(Participant)

    if gender:
        query = query.filter(Participant.gender == gender)
    if name:
        query = query.filter(Participant.name.ilike(f"%{name}%"))
    if surname:
        query = query.filter(Participant.surname.ilike(f"%{surname}%"))

    # Сортировка по дате регистрации
    query = query.order_by(Participant.registration_date.desc())
    participants = query.all()

    # Фильтрация участников по расстоянию
    participants_within_distance = [
        participant for participant in participants
        if calculate_distance(
            current_location[0], current_location[1],
            participant.latitude, participant.longitude
        ) <= max_distance
    ]

    return participants_within_distance


@app.get("/api/list", response_model=List[Participant])
def list_participants(
    filter: ParticipantFilter = Depends(),
    current_user_id: int = Depends(get_current_user_id),
    max_distance: float = 10.0,
    db: Session = Depends(get_db)
):
    # Получаем координаты текущего пользователя
    current_user = db.query(Participant).get(current_user_id)
    current_location = (current_user.latitude, current_user.longitude)

    # Используем кэшированную функцию для получения участников
    participants_within_distance = get_cached_participants(
        filter.gender, filter.name, filter.surname,
        current_location, max_distance, db
    )

    return participants_within_distance
