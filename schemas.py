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

class Patient(Person):
  email: str
  insurance: str 


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

class ShowPatient(ShowPerson):
  email: str
  insurance: str
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
  

class Login(BaseModel):
  username: str
  password: str


class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  username: Optional[str] = None