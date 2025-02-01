#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from app import create_app, db
from app.models.user import User, Vehicle
from app.models.vehicle_health import VehicleHealth
from app.models.service_history import ServiceHistory
from sqlalchemy import inspect

# Load environment variables from .env file
load_dotenv()

# Create the application instance
app = create_app()

def init_db():
    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        # Only create tables if they don't exist
        if not existing_tables:
            db.create_all()
            print("Database initialized with new tables!")
        else:
            print("Database tables already exist, skipping initialization.")

if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Get port from environment variable or use default
    port = int(os.getenv('PORT', 5001))
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=True)
