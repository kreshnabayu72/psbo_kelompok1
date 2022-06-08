from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
  __tablename__ = "blogs"

  id = Column(Integer, primary_key=True, index=True)
  time = Column(String)
  body = Column(String)
  user_id = Column(Integer, ForeignKey("person.id"))

  __mapper_args__ = {
        "polymorphic_identity": "blog",
    }

  creator = relationship("Person", back_populates="blogs")

class Visit(Blog):
  __tablename__ = "visits"

  id = Column(Integer, ForeignKey("blogs.id"), primary_key=True)
  obat = Column(String)
  diagnosis = Column(String)

  __mapper_args__ = {
        "polymorphic_identity": "visit",
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

  blogs = relationship("Blog", back_populates="creator")