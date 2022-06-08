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

  id = Column(Integer, primary_key=True)
  datetime = Column(String)
  status = Column(String)
  note = Column(String)
  patient_id = Column(Integer, ForeignKey("patients.id"))
  doctor_id = Column(Integer, ForeignKey("doctors.id"))

  patient = relationship("Patient", back_populates="requests")
  doctor = relationship("Doctor", back_populates="requests")


class Visit(Base):
  __tablename__ = "visits"

  id = Column(Integer, primary_key=True)
  datetime = Column(String)
  medicine = Column(String)
  diagnosis = Column(String)
  patient_id = Column(Integer, ForeignKey("patients.id"))
  doctor_id = Column(Integer, ForeignKey("doctors.id"))  

  patient = relationship("Patient", back_populates="visits")
  doctor = relationship("Doctor", back_populates="visits")
  

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
  id = Column(Integer, primary_key=True)
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
  id = Column(Integer, primary_key=True)
  id_kki = Column(String)
  specialization = Column(String)
  
  requests = relationship("Request", back_populates="doctor")
  visits = relationship("Visit", back_populates="doctor")

  __mapper_args__ = {
      'polymorphic_identity': 'doctor',
  }

class Medicine(Base):
  __tablename__ = 'medicines'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  efficacy = Column(String)
  side_effect = Column(String)
