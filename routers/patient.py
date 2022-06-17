import schemas, database, models
from hashing import Hash
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash , check_password_hash
from fastapi.encoders import jsonable_encoder

router = APIRouter(
  prefix="/patient",
  tags=['Patient']
)

@router.get('/', response_model=List[schemas.ShowPatient])
def get_all_patient(db: Session = Depends(database.get_db)):
  patient = db.query(models.Patient).all()

  return patient

@router.post('/', response_model=schemas.ShowPatient)
def create_patient(request: schemas.Patient, db: Session = Depends(database.get_db)):
  new_patient = models.Patient(name=request.name, age=request.age,gender=request.gender,address=request.address,telephone=request.telephone, email=request.email,insurance=request.insurance,password=Hash.bcrypt(request.password))
  db.add(new_patient)
  db.commit()
  db.refresh(new_patient)
  return new_patient


@router.get('/visit-list-auth/', response_model=List[schemas.Visit])
def get_all_list(db: Session = Depends(database.get_db),Authorize:AuthJWT=Depends()):

  try:
        Authorize.jwt_required()

  except Exception as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid Token"
    )
  
  subject=Authorize.get_jwt_subject()

  logged_in_patient = db.query(models.Patient).filter(models.Patient.email == subject).first()
  visit= db.query(models.Visit).filter(models.Visit.patient_id == logged_in_patient.id).all()
  
  return visit

@router.post('/login',status_code=200)
async def login(user:schemas.Login,db: Session = Depends(database.get_db),Authorize:AuthJWT=Depends()):
    """     
        ## Login a user
        This requires
            ```
                username:str
                password:str
            ```
        and returns a token pair `access` and `refresh`
    """
    db_user=db.query(models.Patient).filter(models.Patient.email=="string").first()

    if db_user:
        access_token=Authorize.create_access_token(subject=db_user.email)
        refresh_token=Authorize.create_refresh_token(subject=db_user.email)

        response={
            "access":access_token,
            "refresh":refresh_token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid Username Or Password"
    )