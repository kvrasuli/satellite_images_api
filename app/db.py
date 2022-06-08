import os
from motor.motor_asyncio import AsyncIOMotorClient

mongo_url = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(mongo_url)
database = client.fields

collection = database["fields"]
