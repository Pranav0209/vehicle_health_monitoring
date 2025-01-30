from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.models.service_history import ServiceHistory

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    pincode = db.Column(db.String(6))
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    odometer = db.Column(db.Integer, default=0)  # Current odometer reading
    last_service_date = db.Column(db.DateTime)
    next_service_date = db.Column(db.DateTime)
    next_service_mileage = db.Column(db.Integer)
    service_interval_km = db.Column(db.Integer)
    current_mileage = db.Column(db.Integer)
    fuel_type = db.Column(db.String(20))
    
    # Relationships
    health_records = db.relationship('VehicleHealth', backref='vehicle', lazy=True)
    service_history = db.relationship('ServiceHistory', backref='vehicle', lazy=True)

    def __repr__(self):
        return f'<Vehicle {self.registration_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'registration_number': self.registration_number,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'odometer': self.odometer,
            'last_service_date': self.last_service_date.strftime('%Y-%m-%d') if self.last_service_date else None,
            'next_service_date': self.next_service_date.strftime('%Y-%m-%d') if self.next_service_date else None,
            'next_service_mileage': self.next_service_mileage,
            'service_interval_km': self.service_interval_km,
            'current_mileage': self.current_mileage,
            'fuel_type': self.fuel_type
        }

    def update_service_schedule(self):
        """Update service schedule based on latest service history"""
        latest_service = ServiceHistory.query.filter_by(vehicle_id=self.id).order_by(ServiceHistory.service_date.desc()).first()
        if latest_service:
            self.last_service_date = latest_service.service_date
            self.next_service_date = latest_service.next_service_date
            self.next_service_mileage = latest_service.next_service_mileage
