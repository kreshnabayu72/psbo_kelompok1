import enums
from typing import List, Union, Optional
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

class Person(BaseModel):
  name: str
  birthdate: date
  gender: str
  address: str
  telephone: str
  

class Patient(Person):
  email: str
  insurance: str 
  password: str
  class Config():
    orm_mode = True

class Doctor(Person):
  id_kki:str
  specialist:str
  class Config():
    orm_mode = True

class Medicine(BaseModel):
  name: str 
  efficacy: str
  side_effect: str
  class Config():
    orm_mode = True

class ShowMedicine(BaseModel):
  id: int
  name: str 
  efficacy: str
  side_effect: str
  
  class Config():
    orm_mode = True

class InsertMedicine(BaseModel):
  name: str

class Appointment(BaseModel):
  time: datetime
  doctor_db_id: int=1
  patient_id: int=1
  class Config():
    orm_mode = True

class Visit(Appointment):
  diagnosis: str
  _id: Optional[int]
  medicine: Optional[Medicine]

class InsertVisit(Appointment):
  diagnosis: str
  _id: Optional[int]
  medicine: Optional[InsertMedicine]

class Request(Appointment):
  status: enums.Request_Status = enums.Request_Status.Pending
  note: str
 
class Diagnosis(BaseModel):
  symptom: str
  illness: str
  advice: str

class ShowPerson(BaseModel):
  id: int
  name: str
  birthdate: date
  gender: str
  address: str
  telephone: str
  visits: List[Visit] = []
  requests: List[Request] = []
  class Config():
    orm_mode = True

class ShowPersonLite(BaseModel):
  id: int
  name: str
  class Config():
    orm_mode = True

class ShowPatient(ShowPerson):
  email: str
  insurance: str
  class Config():
    orm_mode = True

class ShowDoctor(ShowPerson):
  id_kki: str
  specialist:str
  class Config():
    orm_mode = True

class ShowAppointment(BaseModel):
  id: int
  time: datetime
  patient_id: int
  doctor_db_id: int
  class Config():
    orm_mode = True

class ShowVisit(ShowAppointment):
  diagnosis: str
  medicine_id: Optional[int]
  medicine: Optional[Medicine]

class ShowRequest(ShowAppointment):
  status: enums.Request_Status = enums.Request_Status.Pending
  note: str

  class Config:  
        use_enum_values = True  
  
class Login(BaseModel):
  username: str
  password: str

class Settings(BaseModel):
    authjwt_secret_key:str='b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405'


class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: Optional[str] = None