import asyncio
import os

from dotenv import load_dotenv

load_dotenv()


async def download_image(filename, band):
    downloading_process = await asyncio.create_subprocess_exec(
        "python3",
        "app/utils/image.py",
        "--username",
        os.getenv("COPERNICUS_USERNAME"),
        "--password",
        os.getenv("COPERNICUS_PASSWORD"),
        "--filename",
        filename,
        "--band",
        band,
    )
    await downloading_process.communicate()
