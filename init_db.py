from app import create_app, db
from app.models.user import User, Vehicle
from app.models.vehicle_health import VehicleHealth
from app.models.service_history import ServiceHistory
from sqlalchemy import inspect

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
    init_db()
