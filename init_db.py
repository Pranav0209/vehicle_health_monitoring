from app import create_app, db
from app.models.user import User, Vehicle
from app.models.vehicle_health import VehicleHealth
from app.models.service_history import ServiceHistory

app = create_app()

with app.app_context():
    # Drop all tables
    db.drop_all()
    
    # Create all tables
    db.create_all()
    
    print("Database initialized successfully!")
