import email
import schemas, database, models
from typing import List
from hashing import Hash
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/patient",
  tags=['Patient']
)

@router.post('/', response_model=schemas.Patient, status_code=status.HTTP_201_CREATED)
def create(request: schemas.BasePatient, db: Session = Depends(database.get_db)):
  new_patient = models.Patient(name=request.name, age=request.age, sex=request.sex, address=request.address, phone=request.phone, email=request.email, password=Hash.bcrypt(request.password), insurance=request.insurance)
  db.add(new_patient)
  db.commit()
  db.refresh(new_patient)
  return new_patient

@router.get('/', response_model=List[schemas.ShowPatient], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(database.get_db)):
  patients = db.query(models.Patient).all()
  return patients

@router.get('/{id}', response_model=schemas.ShowPatient)
def show(id: int, db: Session = Depends(database.get_db)):
  patient = db.query(models.Patient).filter(models.Patient.id == id).first()
  if not patient:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with the ID {id} doesn't exists!")
  return patient

@router.put('/{id}', response_model=schemas.Patient, status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.EditPatient, db: Session = Depends(database.get_db)):
  patient = db.query(models.Patient).filter(models.Patient.id == id)
  if not patient.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with the ID {id} doesn't exists!")
  patient.update(request.dict())
  db.commit()
  return patient