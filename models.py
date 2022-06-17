from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime,Date, Enum
from database import Base
from sqlalchemy.orm import relationship,backref
# from sqlalchemy_utils.types import ChoiceType
import enums


class Person(Base):
  __abstract__ = True

  # id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  birthdate = Column(Date)
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

class Diagnosis(Base):
  __tablename__ = "diagnosis"

  id = Column(Integer, primary_key=True, index=True)
  symptom = Column(String)
  illness = Column(String)
  advice = Column(String)

class Appointment(Base):
  __abstract__ = True
  
  time = Column(DateTime)
 
  __mapper_args__ = {
        "polymorphic_identity": "appointment",
    }

class Visit(Appointment):
  __tablename__ = "visit"

  id = Column(Integer, primary_key=True, index=True)
  
  patient_id = Column(Integer, ForeignKey("patient.id"))
  doctor_db_id = Column(Integer, ForeignKey("doctor.id"))
  medicine = relationship("Medicine", backref=backref("visit", uselist=False))
  medicine_id = Column(Integer, ForeignKey("medicine.id"))
  diagnosis = relationship("Diagnosis", backref=backref("visit", uselist=False))
  diagnosis_id = Column(Integer, ForeignKey("diagnosis.id"))
  
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

