import schemas, database, models
from hashing import Hash
from fastapi import APIRouter, Depends, status, HTTPException
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
  new_doctor = models.Doctor(name=request.name, age=request.age,gender=request.gender,address=request.address,telephone=request.telephone, doctor_id=request.doctor_id,specialist=request.specialist,password=Hash.bcrypt(request.password))
  db.add(new_doctor)
  db.commit()
  db.refresh(new_doctor)
  return new_doctor

