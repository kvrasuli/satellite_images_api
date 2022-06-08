import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

async def download_image(filename, band):
    downloading_process = await asyncio.create_subprocess_exec(
        "python3",
        "app/image.py",
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
