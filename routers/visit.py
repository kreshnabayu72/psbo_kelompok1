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


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.InsertVisit, db: Session = Depends(database.get_db)):
  medicine = db.query(models.Medicine).filter(models.Medicine.name == request.medicine.name).first()
  
  try:
    new_visit = models.Visit(time=request.time, diagnosis=request.diagnosis, patient_id=request.patient_id,doctor_db_id=request.doctor_db_id,medicine_id=medicine.id)      

  except Exception as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail="Medicine not found"
    )

  db.add(new_visit)
  db.commit()
  db.refresh(new_visit)
  return new_visit
