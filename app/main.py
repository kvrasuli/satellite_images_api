from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from geojson_pydantic import FeatureCollection
from bson.objectid import ObjectId
import motor.motor_asyncio

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


@app.get("/fields/{id}/image")
async def get_image_for_field():
    field = await db["fields"].find_one({"_id": ObjectId(id)})
