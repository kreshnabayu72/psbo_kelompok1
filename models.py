from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

class Appointment(Base):
  __tablename__ = "appointments"

  id = Column(Integer, primary_key=True, index=True)
  time = Column(DateTime)
  body = Column(String)
  user_id = Column(Integer, ForeignKey("person.id"))

  __mapper_args__ = {
        "polymorphic_identity": "appointment",
    }

  creator = relationship("Person", back_populates="appointments")

class Visit(Appointment):
  __tablename__ = "visits"

  id = Column(Integer, ForeignKey("appointments.id"), primary_key=True)
  obat = Column(String)
  diagnosis = Column(String)

  __mapper_args__ = {
        "polymorphic_identity": "visit",
    }
  
class Request(Appointment):
  __tablename__ = "requests"

  id = Column(Integer, ForeignKey("appointments.id"), primary_key=True)
  status = Column(String)
  note = Column(String)

  __mapper_args__ = {
        "polymorphic_identity": "request",
    }

class Person(Base):
  __tablename__ = 'person'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)
  address = Column(String)
  telephone = Column(String)
  password = Column(String)

  appointments = relationship("Appointment", back_populates="creator")