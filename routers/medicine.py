import schemas, database, models
from hashing import Hash
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
  prefix="/medicine",
  tags=['Medicine']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Medicine, db: Session = Depends(database.get_db)):
  new_medicine = models.Medicine(name=request.name, efficacy=request.efficacy, side_effect=request.side_effect)
  db.add(new_medicine)
  db.commit()
  db.refresh(new_medicine)
  return new_medicine

@router.get('/', response_model=List[schemas.Medicine], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(database.get_db)):
  medicines = db.query(models.Medicine).all()
  return medicines

@router.get('/{id}', response_model=schemas.Medicine, status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(database.get_db)):
  medicine = db.query(models.Medicine).filter(models.Medicine.id == id).first()
  if not medicine:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medicine with the ID {id} doesn't exists!")
  return medicine

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Medicine, db: Session = Depends(database.get_db)):
  medicine = db.query(models.Medicine).filter(models.Medicine.id == id)
  if not medicine.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medicine with the ID {id} doesn't exists!")
  medicine.update(request.dict())
  db.commit()
  return medicine

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db)):
  medicine = db.query(models.Medicine).filter(models.Medicine.id == id)
  if not medicine.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medicine with the ID {id} doesn't exists!")
  medicine.delete(synchronize_session=False)
  db.commit()
  return 'Medicine has been Deleted!'