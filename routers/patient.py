import schemas, database, models
from hashing import Hash
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/patient",
  tags=['Patient']
)


@router.post('/', response_model=schemas.ShowPerson)
def create_person(request: schemas.Person, db: Session = Depends(database.get_db)):
  new_person = models.Person(name=request.name, age=request.age, password=Hash.bcrypt(request.password))
  db.add(new_person)
  db.commit()
  db.refresh(new_person)
  return new_person


@router.get('/{id}', response_model=schemas.ShowPerson)
def get_person(id: int, db: Session = Depends(database.get_db)):
  person = db.query(models.Person).filter(models.Person.id == id).first()
  if not person:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} isn't found!")
  return person