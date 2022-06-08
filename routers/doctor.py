import schemas, database, models
from typing import List
from hashing import Hash
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/doctor",
  tags=['Doctor']
)

@router.post('/', response_model=schemas.Doctor, status_code=status.HTTP_201_CREATED)
def create(request: schemas.Doctor, db: Session = Depends(database.get_db)):
  new_doctor = models.Doctor(name=request.name, age=request.age, sex=request.sex, address=request.address, phone=request.phone, id_kki=request.id_kki, specialization=request.specialization)
  db.add(new_doctor)
  db.commit()
  db.refresh(new_doctor)
  return new_doctor

@router.get('/', response_model=List[schemas.ShowDoctor], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(database.get_db)):
  doctor = db.query(models.Doctor).all()
  return doctor

@router.get('/{id}', response_model=schemas.ShowDoctor)
def show(id: int, db: Session = Depends(database.get_db)):
  doctor = db.query(models.Doctor).filter(models.Doctor.id == id).first()
  if not doctor:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor with the ID {id} doesn't exists!")
  return doctor

@router.put('/{id}', response_model=schemas.Doctor, status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Doctor, db: Session = Depends(database.get_db)):
  doctor = db.query(models.Doctor).filter(models.Doctor.id == id)
  if not doctor.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor with the ID {id} doesn't exists!")
  doctor.update(request.dict())
  db.commit()
  return doctor