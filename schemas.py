from typing import List, Union, Optional
from pydantic import BaseModel


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


class BlogBase(BaseModel):
  id: int
  time: str
  body: str
  

class Blog(BlogBase):
  class Config():
    orm_mode = True

class Visit(Blog):
  obat: str
  diagnosis: str

class ShowPerson(BaseModel):
  id: int
  name: str
  age: int
  gender: str
  address: str
  telephone: str
  blogs: List[Blog] = []
  class Config():
    orm_mode = True

class ShowPatient(ShowPerson):
  email: str
  insurance: str
  visits: List[Visit] = [] 

class ShowBlog(BaseModel):
  time: str
  body: str
  creator: ShowPerson
  class Config():
    orm_mode = True

class ShowVisit(ShowBlog):
  obat: str
  diagnosis: str

class Login(BaseModel):
  username: str
  password: str


class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  username: Optional[str] = None