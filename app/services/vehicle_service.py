from app.models import Vehicle

def add_vehicle(user_id, registration_number, make, model, year, purchase_date):
    vehicle = Vehicle(
        user_id=user_id, 
        registration_number=registration_number, 
        make=make,
        model=model, 
        year=year, 
        purchase_date=purchase_date
    )
    db.session.add(vehicle)
    db.session.commit()

def get_vehicles(user_id):
    return Vehicle.query.filter_by(user_id=user_id).all()
