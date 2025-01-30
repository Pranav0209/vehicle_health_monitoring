from app import db
from datetime import datetime

class ServiceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    service_date = db.Column(db.DateTime, nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)  # Odometer reading at service
    cost = db.Column(db.Float, nullable=True)
    service_center = db.Column(db.String(100), nullable=True)
    next_service_date = db.Column(db.DateTime, nullable=True)
    next_service_mileage = db.Column(db.Integer, nullable=True)
    
    def __init__(self, vehicle_id, service_date, service_type, description, mileage,
                 cost=None, service_center=None, next_service_date=None, next_service_mileage=None):
        self.vehicle_id = vehicle_id
        self.service_date = service_date
        self.service_type = service_type
        self.description = description
        self.mileage = mileage
        self.cost = cost
        self.service_center = service_center
        self.next_service_date = next_service_date
        self.next_service_mileage = next_service_mileage

    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'service_date': self.service_date.strftime('%Y-%m-%d'),
            'service_type': self.service_type,
            'description': self.description,
            'mileage': self.mileage,
            'cost': self.cost,
            'service_center': self.service_center,
            'next_service_date': self.next_service_date.strftime('%Y-%m-%d') if self.next_service_date else None,
            'next_service_mileage': self.next_service_mileage
        }
