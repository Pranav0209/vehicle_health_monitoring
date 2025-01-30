from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app import db

class Vehicle:
    def __init__(self, registration_number, make, model, year, purchase_date):
        self.registration_number = registration_number
        self.make = make
        self.model = model
        self.year = year
        self.purchase_date = purchase_date

