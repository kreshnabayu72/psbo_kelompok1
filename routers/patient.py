import schemas, database, models
from hashing import Hash
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
  prefix="/patient",
  tags=['Patient']
)

@router.get('/', response_model=List[schemas.ShowPatient])
def get_all_patient(db: Session = Depends(database.get_db)):
  patient = db.query(models.Patient).all()

  return patient

@router.post('/', response_model=schemas.ShowPatient)
def create_patient(request: schemas.Patient, db: Session = Depends(database.get_db)):
  new_patient = models.Patient(name=request.name, age=request.age,gender=request.gender,address=request.address,telephone=request.telephone, email=request.email,insurance=request.insurance,password=Hash.bcrypt(request.password))
  db.add(new_patient)
  db.commit()
  db.refresh(new_patient)
  return new_patient

