from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app import db

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    vehicles = relationship("Vehicle", back_populates="user")
