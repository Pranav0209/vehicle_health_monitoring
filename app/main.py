from app import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from app.models.user import User, Vehicle
        from app.models.vehicle_health import VehicleHealth
        from app import db
        db.create_all()
    app.run(debug=True, port=5002)