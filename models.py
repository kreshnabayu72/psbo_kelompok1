from collections import UserList
from datetime import datetime
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Boolean, DateTime
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

# class Appointment(Base):
#   __abstract__ = True

#   id = Column(Integer, primary_key=True, index=True)
#   time = Column(DateTime)
  
#   patient_id = Column(Integer, ForeignKey("patients.id"))
#   doctor_id = Column(Integer, ForeignKey("doctors.id"))

#   __mapper_args__ = {
#         "polymorphic_identity": "appointment",
#     }

#   creator = relationship("Person", back_populates="appointments")

class Request(Base):
  __tablename__ = "requests"

  id = Column(Integer, primary_key=True, index=True)
  datetime = Column(String)
  status = Column(String)
  note = Column(String)
  patient_id = Column(Integer, ForeignKey("patients.id"))
  doctor_id = Column(Integer, ForeignKey("doctors.id"))

  patient = relationship("Patient", back_populates="requests", uselist=False)
  doctor = relationship("Doctor", back_populates="requests", uselist=False)


class Visit(Base):
  __tablename__ = "visits"

  id = Column(Integer, primary_key=True, index=True)
  datetime = Column(String)
  patient_id = Column(Integer, ForeignKey("patients.id"))
  doctor_id = Column(Integer, ForeignKey("doctors.id"))  

  patient = relationship("Patient", back_populates="visits", uselist=False)
  doctor = relationship("Doctor", back_populates="visits", uselist=False)
  diagnosis = relationship("Diagnosis", back_populates="visits", uselist=False)
  medicine = relationship("Medicine", back_populates="visits")
  

# class Person(Base):
#   __tablename__ = 'person'

#   id = Column(Integer, primary_key=True, index=True)
#   name = Column(String)
#   age = Column(Integer)
#   gender = Column(String)
#   address = Column(String)
#   telephone = Column(String)
#   password = Column(String)

#   requests = relationship("Appointment", back_populates="creator")

class Person_(Base):
  __abstract__ = True

  # TYPES = [('male', 'Male'), ('female', 'Female')]
  name = Column(String)
  # dobirth = Column(Date)
  age = Column(Integer)
  sex = Column(String)
  address = Column(String)
  phone = Column(String)

class Patient(Person_):
  __tablename__ = 'patients'
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String)
  password = Column(String)
  insurance = Column(String)

  requests = relationship("Request", back_populates="patient")
  visits = relationship("Visit", back_populates="patient")

  __mapper_args__ = {
      'polymorphic_identity': 'patient',
  }

class Doctor(Person_):
  __tablename__ = 'doctors'
  id = Column(Integer, primary_key=True, index=True)
  id_kki = Column(String)
  specialization = Column(String)
  
  requests = relationship("Request", back_populates="doctor")
  visits = relationship("Visit", back_populates="doctor")

  __mapper_args__ = {
      'polymorphic_identity': 'doctor',
  }

class Diagnosis(Base):
  __tablename__ = 'diagnoses'

  id = Column(Integer, primary_key=True, index=True)
  symptom = Column(String)
  disease = Column(String)
  suggestion = Column(String)
  visit_id = Column(Integer, ForeignKey("visits.id"))

  visit = relationship("Visit", back_populates="diagnosis")

class Medicine(Base):
  __tablename__ = 'medicines'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  efficacy = Column(String)
  side_effect = Column(String)

  visit = relationship("Visit", back_populates="medicine")
  