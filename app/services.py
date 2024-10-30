import os
from fastapi import UploadFile

from .config import settings
from .image_utils import add_watermark_async


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
