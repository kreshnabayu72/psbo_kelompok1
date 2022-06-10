import schemas, database, models, enums
from hashing import Hash
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
  prefix="/person",
  tags=['Persons']
)


# @router.get('/', response_model=List[schemas.ShowPerson])
# def get_all_person(db: Session = Depends(database.get_db)):
#   person = db.query(models.Person).all()
#   return person

# @router.get('/{id}', response_model=schemas.ShowPerson)
# def get_person(id: int, db: Session = Depends(database.get_db)):
#   person = db.query(models.Person).filter(models.Person.id == id).first()
#   if not person:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} isn't found!")
#   return person