import schemas, database, models
from hashing import Hash
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
  prefix="/person",
  tags=['Persons']
)


@router.post('/', response_model=schemas.ShowPerson)
def create_person(request: schemas.Person, db: Session = Depends(database.get_db)):
  new_person = models.Person(name=request.name, age=request.age,gender=request.gender,address=request.address,telephone=request.telephone, password=Hash.bcrypt(request.password))
  db.add(new_person)
  db.commit()
  db.refresh(new_person)
  return new_person

@router.get('/', response_model=List[schemas.ShowPerson])
def get_person(db: Session = Depends(database.get_db)):
  person = db.query(models.Person).all()
  return person

@router.get('/{id}', response_model=schemas.ShowPerson)
def get_person(id: int, db: Session = Depends(database.get_db)):
  person = db.query(models.Person).filter(models.Person.id == id).first()
  if not person:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} isn't found!")
  return person