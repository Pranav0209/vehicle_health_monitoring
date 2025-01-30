#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from app import create_app, db
from app.models.user import User, Vehicle
from app.models.vehicle_health import VehicleHealth
from app.models.service_history import ServiceHistory

# Load environment variables from .env file
load_dotenv()

# Create the application instance
app = create_app()

def init_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Get port from environment variable or use default
    port = int(os.getenv('PORT', 5000))
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=True)
