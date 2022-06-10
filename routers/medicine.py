import schemas, database, models
from hashing import Hash
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
  prefix="/medicine",
  tags=['Medicine']
)

@router.get('/', response_model=List[schemas.ShowMedicine])
def get_all_medicine(db: Session = Depends(database.get_db)):
  medicine = db.query(models.Medicine).all()

  return medicine

@router.post('/', response_model=schemas.ShowMedicine)
def create_medicine(request: schemas.Medicine, db: Session = Depends(database.get_db)):
  new_medicine = models.Medicine(name=request.name, function=request.function)
  db.add(new_medicine)
  db.commit()
  db.refresh(new_medicine)
  return new_medicine

