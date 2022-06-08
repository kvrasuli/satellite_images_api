import aiofiles
from bson import json_util
from bson.objectid import ObjectId
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, Response
from geojson_pydantic import FeatureCollection

from app.db import collection
from app.utils.download import download_image

router = APIRouter()


@router.post("/", status_code=201)
async def create_field(field: FeatureCollection = Body(...)):
    field = jsonable_encoder(field)
    new_field = await collection.insert_one(field)
    created_field = await collection.find_one({"_id": new_field.inserted_id})
    created_field["id"] = str(created_field["_id"])
    created_field.pop("_id")
    return created_field


@router.get("/{id}", response_model=FeatureCollection)
async def get_field(id: str):
    field = await collection.find_one({"_id": ObjectId(id)})
    if field:
        return field
    raise HTTPException(status_code=404)


@router.delete("/{id}", status_code=204, response_class=Response)
async def delete_field(id: str):
    field = await collection.delete_one({"_id": ObjectId(id)})
    if field.deleted_count == 1:
        return
    raise HTTPException(status_code=404)


@router.get("/{id}/ndvi")
async def get_ndvi_for_field():
    field = await collection.find_one({"_id": ObjectId(id)})


@router.get("/{id}/image/{band}")
async def get_image_for_field(id: str, band: str):
    field = await collection.find_one({"_id": ObjectId(id)})
    async with aiofiles.open(f"{field['_id']}.geojson", mode="w") as file:
        await file.write(json_util.dumps(field))
    filename = f"{field['_id']}.geojson"
    await download_image(filename, band)
    return FileResponse(f"{filename}_band{band}.jp2")
