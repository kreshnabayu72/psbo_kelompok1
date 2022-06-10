import schemas, database, models,enums
from oauth2 import get_current_user
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session


router = APIRouter(
  prefix="/request",
  tags=['Requests']
)

@router.get('/', response_model=List[schemas.ShowRequest])
def all(db: Session = Depends(database.get_db)):
  requests = db.query(models.Request).all()
  return requests


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Request, db: Session = Depends(database.get_db)):
  # new_request = models.Request(time=request.time,status=request.status, note=request.note, patient_id=1,doctor_id=1)
  new_request = models.Request(time=request.time,status=request.status, note=request.note, patient_id=1,doctor_db_id=1)
  db.add(new_request)
  db.commit()
  db.refresh(new_request)
  return new_request
