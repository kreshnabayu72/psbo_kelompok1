import schemas, database, models
from oauth2 import get_current_user
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/visit",
  tags=['Visits']
)

@router.get('/', response_model=List[schemas.ShowVisit])
def all(db: Session = Depends(database.get_db)):
  visits = db.query(models.Visit).all()
  return visits


@router.post('/', status_code=status.HTTP_201_CREATED,response_model=schemas.ShowVisit)
def create(request: schemas.InsertVisit, db: Session = Depends(database.get_db)):
  medicine = db.query(models.Medicine).filter(models.Medicine.id == request.medicine.id)
  
  if not medicine.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Medicine not found")
  diagnosis = models.Diagnosis(symptom=request.diagnosis.symptom,illness=request.diagnosis.illness,advice=request.diagnosis.advice)
  db.add(diagnosis)
  db.commit()
  db.refresh(diagnosis)

  new_visit = models.Visit(time=request.time, diagnosis_id=diagnosis.id, patient_id=request.patient_id, doctor_db_id=request.doctor_db_id,medicine_id=request.medicine.id)      
  
  db.add(new_visit)
  db.commit()
  db.refresh(new_visit)
  return new_visit
