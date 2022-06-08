import aiofiles
import motor.motor_asyncio
from bson.objectid import ObjectId
from bson import json_util
from fastapi import Body, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, Response
from geojson_pydantic import FeatureCollection

from app.download import download_image

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.fields

app = FastAPI()


@app.post("/fields/", status_code=201)
async def create_field(field: FeatureCollection = Body(...)):
    field = jsonable_encoder(field)
    new_field = await db["fields"].insert_one(field)
    created_field = await db["fields"].find_one({"_id": new_field.inserted_id})
    created_field["id"] = str(created_field["_id"])
    created_field.pop("_id")
    return created_field


@app.get("/fields/{id}", response_model=FeatureCollection)
async def get_field(id: str):
    field = await db["fields"].find_one({"_id": ObjectId(id)})
    if field:
        return field
    raise HTTPException(status_code=404)


@app.delete("/fields/{id}", status_code=204, response_class=Response)
async def delete_field(id: str):
    field = await db["fields"].delete_one({"_id": ObjectId(id)})
    if field.deleted_count == 1:
        return
    raise HTTPException(status_code=404)


@app.get("/fields/{id}/ndvi")
async def get_ndvi_for_field():
    field = await db["fields"].find_one({"_id": ObjectId(id)})


@app.get("/fields/{id}/image/{band}")
async def get_image_for_field(id: str, band: str):
    field = await db["fields"].find_one({"_id": ObjectId(id)})
    async with aiofiles.open(f"{field['_id']}.geojson", mode="w") as file:
        await file.write(json_util.dumps(field))
    filename = f"{field['_id']}.geojson"
    await download_image(filename, band)
    return FileResponse(f"{filename}_band{band}.jp2")