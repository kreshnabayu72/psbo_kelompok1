from typing import List, Union, Optional
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta
from enum import Enum

class Person(BaseModel):
  name: str
  age: int
  gender: str
  address: str
  telephone: str
  password: str

class Person_(BaseModel):  
  name: str
  age: int
  sex: str
  address: str
  phone: str

class BasePatient(Person_):
  email: str
  password: str
  insurance: Optional[str]

class EditPatient(Person_):
  insurance: Optional[str]
  class Config():
    orm_mode = True

class Patient(Person_):
  email: str
  class Config():
    orm_mode = True

class Doctor(Person_):
  id_kki: str
  specialization: str
  class Config():
    orm_mode = True

# ================================================>

class AppointmentBase(BaseModel):
  id: int
  time: datetime
  body: str
  

class Appointment(AppointmentBase):
  class Config():
    orm_mode = True

class Visit(Appointment):
  obat: str
  diagnosis: str

class Request(Appointment):
  status: str = "PENDING"
  note: str

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

class ShowPatient(Patient):
  requests: List[Request] = []
  visits: List[Visit] = [] 

class ShowDoctor(Doctor):
  requests: List[Request] = []
  visits: List[Visit] = []

class ShowAppointment(BaseModel):
  time: datetime
  body: str
  creator: ShowPerson
  class Config():
    orm_mode = True

class ShowVisit(ShowAppointment):
  obat: str
  diagnosis: str

class Request_Status(str,Enum):
  pending="pending"
  acc="acc"
  no="no"

class ShowRequest(ShowAppointment):
  status: str
  note: str

  class Config:  
        use_enum_values = True  # <--
  
class Medicine(BaseModel):
  name: str
  efficacy: str
  side_effect: str
  class Config():
    orm_mode = True





class Login(BaseModel):
  username: str
  password: str


class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  username: Optional[str] = None