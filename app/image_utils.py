import asyncio
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

executor = ThreadPoolExecutor(max_workers=2)


async def add_watermark_async(
    input_image_path: str, watermark_path: str, output_image_path: str
):
    """Асинхронно накладывает водяной знак на изображение."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        executor, add_watermark, input_image_path,
        watermark_path, output_image_path
    )


def add_watermark(
    input_image_path: str, watermark_path: str, output_image_path: str
):
    """Синхронная функция для наложения водяного знака на изображение."""
    with Image.open(input_image_path) as base_image:
        with Image.open(watermark_path) as watermark:
            base_image.paste(watermark, (0, 0), watermark)
            base_image.save(output_image_path)
