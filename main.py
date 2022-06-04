import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
import datetime

MONGODB_URL="localhost:27017"
app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.PSBO


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Appointment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    time: str
    dokter: str
    pasien: str
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "time": "30 September 1965",
                "dokter": "dokter a",
                "pasien": "pasien a",
            }
        }

class Request(Appointment):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    status: Optional[bool]
    note:str
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "time": "30 September 1965",
                "dokter": "dokter a",
                "pasien": "pasien a",
                "status": None,
                "note": "Sebaiknya tidak usah mandi jendral"
            }
        }

class UpdateRequest(Appointment):
    status: Optional[bool]
    note: Optional[str]
    time: Optional[str]
    dokter: Optional[str]
    pasien: Optional[str]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "status": True,
            }
        }

class Visit(Appointment):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    obat:str
    diagnosis:str
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "time": "30 September 1965",
                "dokter": "dokter a",
                "pasien": "pasien a",
                "obat": "Panadol",
                "diagnosis": "Stress projekan"
            }
        }


@app.get("/")
def index():
    return "Hello world"

@app.post("/ajukan-janji")
async def ajukan_janji(request:Request=Body(...)):
    request = jsonable_encoder(request)
    new_request = await db["requests"].insert_one(request)
    created_request = await db["requests"].find_one({"_id": new_request.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_request)

@app.put("/confirm-janji/{id}",response_description="Konfirmasi janji")
async def confirm_janji(id:str,request:UpdateRequest=Body(...)):
    update_result = await db["requests"].update_one({"_id": id}, {"$set": {"status":request.status}})
    new_result = await db["requests"].find_one({"_id": id})
    return new_result

@app.get("/list-kunjungan",response_description="List all appointment", response_model=List[Appointment])
async def get_kunjungan():
    kunjungan = await db["appointments"].find().to_list(1000)
    return kunjungan

