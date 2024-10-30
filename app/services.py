import os
from datetime import date

from fastapi import HTTPException, UploadFile
from geopy.distance import great_circle
from sqlalchemy.orm import Session

from .config import settings
from .models import Participant
from .image_utils import add_watermark_async

DAILY_LIKE_LIMIT = 10


async def save_avatar_with_watermark(
    avatar: UploadFile, output_dir: str = "/tmp"
):
    """Сохраняет загруженный файл с наложенным водяным знаком."""
    input_path = os.path.join(output_dir, avatar.filename)
    output_path = os.path.join(output_dir, f"watermarked_{avatar.filename}")
    watermark_path = settings.WATERMARK_PATH

    with open(input_path, "wb") as file:
        file.write(await avatar.read())

    await add_watermark_async(input_path, watermark_path, output_path)
    return output_path


def check_daily_like_limit(
    participant: Participant, db: Session
):
    """Проверяет дневной лимит лайков."""
    today = date.today()
    if participant.last_like_date != today:
        participant.last_like_date = today
        participant.daily_likes_count = 0

    # Проверяем, не достигнут ли лимит лайков
    if participant.daily_likes_count >= DAILY_LIKE_LIMIT:
        raise HTTPException(
            status_code=400,
            detail="Вы достигли лимита лайков на сегодня."
        )

    participant.daily_likes_count += 1
    db.commit()


def calculate_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
):
    """Вычисляет дистанцию между участниками."""
    return great_circle((lat1, lon1), (lat2, lon2)).kilometers
