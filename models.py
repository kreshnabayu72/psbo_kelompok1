from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Enum
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
import enums


class Person(Base):
  __abstract__ = True

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)
  address = Column(String)
  telephone = Column(String)
  password = Column(String)


class Patient(Person):
  __tablename__ = 'patient'

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String)
  insurance = Column(String)

  __mapper_args__ = {
        "polymorphic_identity": "patient",
        "concrete": True
    }
  
  visits = relationship("Visit", backref="patient")
  requests = relationship("Request", backref="patient")

class Doctor(Person):
  __tablename__ = 'doctor'
  
  id = Column(Integer, primary_key=True, index=True)
  # person_id = Column(Integer, ForeignKey("person.id"), primary_key=True)
  doctor_id = Column(String)
  specialist = Column(String)

  __mapper_args__ = {
        "polymorphic_identity": "doctor",
        "concrete": True
    }

  visits = relationship("Visit", backref="doctor")
  requests = relationship("Request", backref="doctor")


class Appointment(Base):
  __tablename__ = "appointments"

  id = Column(Integer, primary_key=True, index=True)
  time = Column(DateTime)
 
  __mapper_args__ = {
        "polymorphic_identity": "appointment",
    }

class Visit(Appointment):
  __tablename__ = "visit"

  id = Column(Integer, primary_key=True, index=True)
  time = Column(DateTime)
  patient_id = Column(Integer, ForeignKey("patient.id"))
  doctor_db_id = Column(Integer, ForeignKey("doctor.id"))
  obat = Column(String)
  diagnosis = Column(String)

  # medicine = relationship("Medicine")
  __mapper_args__ = {
        "polymorphic_identity": "visit",
        "concrete": True
    }
  
class Request(Appointment):
  __tablename__ = "requests"

  id = Column(Integer, primary_key=True, index=True)
  time = Column(DateTime)
  patient_id = Column(Integer, ForeignKey("patient.id"))
  doctor_db_id = Column(Integer, ForeignKey("doctor.id"))
  status = Column(Enum(enums.Request_Status))
  note = Column(String)

  __mapper_args__ = {
        "polymorphic_identity": "request",
        "concrete": True
    }

class Medicine(Base):
  __tablename__ = "medicine"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  function = Column(String)