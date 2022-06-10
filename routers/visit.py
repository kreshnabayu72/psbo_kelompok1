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
def create(request: schemas.Visit, db: Session = Depends(database.get_db)):
  new_visit = models.Visit(time=request.time,obat=request.obat, diagnosis=request.diagnosis, patient_id=1,doctor_db_id=1,medicine_id=1)
  db.add(new_visit)
  db.commit()
  db.refresh(new_visit)
  return new_visit
