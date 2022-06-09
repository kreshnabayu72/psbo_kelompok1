import enums
from typing import List, Union, Optional
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

class Person(BaseModel):
  id: int
  name: str
  age: int
  gender: str
  address: str
  telephone: str
  password: str

class Patient(Person):
  email: str
  insurance: str 

class Doctor(Person):
  doctor_id:str
  specialist:str


class AppointmentBase(BaseModel):
  id: int
  time: datetime

class Appointment(AppointmentBase):
  class Config():
    orm_mode = True
    

class Visit(Appointment):
  obat: str
  diagnosis: str

class Request(Appointment):
  status: enums.Request_Status = enums.Request_Status.Pending
  note: str

class Medicine(BaseModel):
  id: int
  name: str 
  function: str
  class Config():
    orm_mode = True
  
class Diagnosis(BaseModel):
  symptom: str
  illness: str
  advice: str

class ShowPerson(BaseModel):
  id: int
  name: str
  age: int
  gender: str
  address: str
  telephone: str
  appointments: List[Appointment] = []
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
  doctor_id:str
  specialist:str
  class Config():
    orm_mode = True

class ShowAppointment(BaseModel):
  id: int
  time: datetime
  patient: ShowPersonLite
  doctor: ShowPersonLite
  class Config():
    orm_mode = True

class ShowVisit(ShowAppointment):
  obat: str
  diagnosis: str


class ShowRequest(ShowAppointment):
  status: enums.Request_Status = enums.Request_Status.Pending
  note: str

  class Config:  
        use_enum_values = True  # <--
  

class Login(BaseModel):
  username: str
  password: str


class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  username: Optional[str] = None