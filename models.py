from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Enum
from database import Base
from sqlalchemy.orm import relationship,backref
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


class Patient(Person):
  __tablename__ = 'patient'

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String)
  insurance = Column(String)
  password = Column(String)

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
  id_kki = Column(String)
  specialist = Column(String)

  __mapper_args__ = {
        "polymorphic_identity": "doctor",
        "concrete": True
    }

  visits = relationship("Visit", backref="doctor")
  requests = relationship("Request", backref="doctor")

class Medicine(Base):
  __tablename__ = "medicine"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  efficacy = Column(String)
  side_effect = Column(String)

class Appointment(Base):
  __abstract__ = True
  
  time = Column(DateTime)
 
  __mapper_args__ = {
        "polymorphic_identity": "appointment",
    }

class Visit(Appointment):
  __tablename__ = "visit"

  id = Column(Integer, primary_key=True, index=True)
  diagnosis = Column(String)
  
  patient_id = Column(Integer, ForeignKey("patient.id"))
  doctor_db_id = Column(Integer, ForeignKey("doctor.id"))
  medicine = relationship("Medicine", backref=backref("visit", uselist=False))
  medicine_id = Column(Integer, ForeignKey("medicine.id"))
  
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

