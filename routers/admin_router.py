import os
from bson import ObjectId
import inspect
from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter,Body,FastAPI
from typing import Optional, List
import motor.motor_asyncio

router = APIRouter()

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


@router.get("/list-pasien")
def nama_fungsi():
    return {"Tes":123}

@router.get("/list-dokter")
def nama_fungsi():
    return {"Tes":123}

@router.get("/list-kunjungan",response_description="List all appointment", response_model=List[Appointment])
async def get_kunjungan():
    kunjungan = await db["appointments"].find().to_list(1000)
    return kunjungan

@router.get("/list-obat")
def nama_fungsi():
    return {"Tes":123}

#POST LIST-DOKter AJA?
@router.post("/manajemen-dokter")
def nama_fungsi():
    return {"Tes":123}
