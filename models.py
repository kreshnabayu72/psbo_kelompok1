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

  # appointments = relationship("Appointment", back_populates="patient")

class Patient(Person):
  __tablename__ = 'patient'

  # person_id = Column(Integer, ForeignKey("person.id"), primary_key=True)
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String)
  insurance = Column(String)

  __mapper_args__ = {
        "polymorphic_identity": "patient",
        "concrete": True
    }
  appointments = relationship("Appointment", back_populates="patient")

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

  appointments = relationship("Appointment", back_populates="doctor")


class Appointment(Base):
  __tablename__ = "appointments"

  id = Column(Integer, primary_key=True, index=True)
  time = Column(DateTime)
  patient_id = Column(Integer, ForeignKey("patient.id"))
  doctor_id = Column(Integer, ForeignKey("doctor.id"))

  __mapper_args__ = {
        "polymorphic_identity": "appointment",
    }

  patient = relationship("Patient", back_populates="appointments")
  doctor = relationship("Doctor", back_populates="appointments")

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
  status = Column(Enum(enums.Request_Status))
  note = Column(String)

  __mapper_args__ = {
        "polymorphic_identity": "request",
    }
  
class Medicine(Base):
  __tablename__ = "medicine"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  function = Column(String)