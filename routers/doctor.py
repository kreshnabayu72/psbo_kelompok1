from pydoc import doc

from requests import Response
import schemas, database, models
from hashing import Hash
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
  prefix="/doctor",
  tags=['Doctor']
)

@router.get('/', response_model=List[schemas.ShowDoctor])
def get_all_doctor(db: Session = Depends(database.get_db)):
  doctor = db.query(models.Doctor).all()

  return doctor

@router.post('/', response_model=schemas.ShowDoctor)
def create_doctor(request: schemas.Doctor, db: Session = Depends(database.get_db)):
  new_doctor = models.Doctor(name=request.name, age=request.age,gender=request.gender,address=request.address,telephone=request.telephone, id_kki=request.id_kki,specialist=request.specialist)
  db.add(new_doctor)
  db.commit()
  db.refresh(new_doctor)
  return new_doctor

@router.get('/{id}', response_model=schemas.ShowDoctor)
def show(id: int, db: Session = Depends(database.get_db)):
  doctor = db.query(models.Doctor).filter(models.Doctor.id == id).first()
  if not doctor:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor with the ID {id} doesn't exists!")
  return doctor

@router.put('/update/{id}', response_model=schemas.ShowDoctor)
def update(id: int, request: schemas.Doctor, db: Session = Depends(database.get_db)):
  doctor = db.query(models.Doctor).filter(models.Doctor.id == id)
  if not doctor.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor with the ID {id} doesn't exists!")
  # tmp = jsonable_encoder(request)
  doctor.update(request.dict())
  db.commit()
  respons = db.query(models.Doctor).filter(models.Doctor.id == id).first()
  return respons