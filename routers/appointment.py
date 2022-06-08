import schemas, database, models
from oauth2 import get_current_user
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/appointment",
  tags=['Appointments']
)

@router.get('/', response_model=List[schemas.ShowAppointment])
def all(db: Session = Depends(database.get_db)):
  appointments = db.query(models.Appointment).all()
  return appointments


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Appointment, db: Session = Depends(database.get_db)):
  new_appointment = models.Appointment(time=request.time, body=request.body, user_id=1)
  db.add(new_appointment)
  db.commit()
  db.refresh(new_appointment)
  return new_appointment


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db)):
  appointment = db.query(models.Appointment).filter(models.Appointment.id == id)
  if not appointment.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointment with the id {id} isn't found!")
  appointment.delete(synchronize_session=False)
  db.commit()
  return 'appointment has been deleted!'


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Appointment, db: Session = Depends(database.get_db)):
  appointment = db.query(models.Appointment).filter(models.Appointment.id == id)
  if not appointment.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointment with the id {id} isn't found!")
  appointment.update(request.dict())
  db.commit()
  return 'appointment updated!'


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowAppointment)
def show(id, db: Session = Depends(database.get_db)):
  appointment = db.query(models.Appointment).filter(models.Appointment.id == id).first()
  if not appointment:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointment with the id {id} isn't available")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f"Appointment with the id {id} isn't available"}
  return appointment