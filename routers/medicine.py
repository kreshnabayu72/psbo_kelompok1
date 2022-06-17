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


@router.get('/{id}',response_model=schemas.ShowMedicine)
def get_medicine(id:int, db:Session = Depends(database.get_db)):
  med = db.query(models.Medicine).filter(models.Medicine.id == id)
  if not med:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medicine with the ID {id} doesn't exists!")
  return med.first()

@router.post('/', response_model=schemas.ShowMedicine)
def create_medicine(request: schemas.Medicine, db: Session = Depends(database.get_db)):
  new_medicine = models.Medicine(name=request.name, efficacy=request.efficacy,side_effect=request.side_effect)
  db.add(new_medicine)
  db.commit()
  db.refresh(new_medicine)
  return new_medicine

@router.put('/update/{id}', response_model=schemas.ShowMedicine)
def update(id:int, request: schemas.Medicine, db: Session = Depends(database.get_db)):
  med = db.query(models.Medicine).filter(models.Medicine.id == id)
  if not med:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medicine with the ID {id} doesn't exists!")
  med.update(request.dict())
  db.commit()
  tmp = db.query(models.Medicine).filter(models.Medicine.id == id).first()
  return tmp 

@router.delete('/delete/{id}')
def delete(id:int, db: Session = Depends(database.get_db)):
  med = db.query(models.Medicine).filter(models.Medicine.id == id)
  if not med:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medicine with the ID {id} doesn't exists!")
  med.delete()
  db.commit()
  return 'Medicine Has Been Updated!'