from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.user import Vehicle,ServiceHistory
from app.models.vehicle_health import VehicleHealth
from app import db
from datetime import datetime
import requests
import os

api = Blueprint('api', __name__)

@api.route('/vehicle/<int:vehicle_id>/health', methods=['POST'])
@login_required
def update_vehicle_health(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if vehicle.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    
    # Create new health record with all parameters
    health_record = VehicleHealth(
        vehicle_id=vehicle_id,
        engine_rpm=data.get('engine_rpm', 0),
        oil_pressure=data.get('oil_pressure', 0),
        fuel_pressure=data.get('fuel_pressure', 0),
        coolant_pressure=data.get('coolant_pressure', 0),
        oil_temperature=data.get('oil_temperature', 0),
        coolant_temperature=data.get('coolant_temperature', 0),
        air_temperature=data.get('air_temperature', 298),
        process_temperature=data.get('process_temperature', 308),
        rotation_speed=data.get('rotation_speed', 1500),
        torque=data.get('torque', 40),
        tool_wear=data.get('tool_wear', 0)
    )
    
    db.session.add(health_record)
    db.session.commit()
    
    response = health_record.to_dict()
    
    # Add action items based on analysis
    action_items = []
    
    # Check engine condition
    if response['condition'] == 'critical':
        action_items.append({
            'severity': 'high',
            'message': f'Engine in critical condition! Immediate attention required.',
            'action': 'Contact service center immediately'
        })
    
    # Check maintenance needs
    if response['maintenance_needed']:
        action_items.append({
            'severity': 'medium',
            'message': f'Maintenance needed: {response["failure_type"]}',
            'action': 'Schedule maintenance appointment'
        })
    
    # Add critical components
    for component in response['critical_components']:
        action_items.append({
            'severity': 'high' if response['severity'] == 'high' else 'medium',
            'message': f'{component["name"]} outside normal range (Current: {component["current"]}, Range: {component["min"]}-{component["max"]})',
            'action': f'Check {component["name"].lower()} and service if needed'
        })
    
    response['action_items'] = action_items
    return jsonify(response)

@api.route('/vehicle/<int:vehicle_id>/health/history', methods=['GET'])
@login_required
def get_vehicle_health_history(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if vehicle.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get last 24 hours of health records
    health_records = VehicleHealth.query.filter_by(vehicle_id=vehicle_id)\
        .order_by(VehicleHealth.timestamp.desc())\
        .limit(24)\
        .all()
    
    return jsonify([record.to_dict() for record in health_records])

@api.route('/garages/search', methods=['POST'])
@login_required
def search_garages():
    data = request.json
    pincode = data.get('pincode', current_user.pincode)
    
    # Use a geocoding service to get coordinates from pincode
    GEOCODING_API_KEY = os.getenv('GEOCODING_API_KEY', 'your-api-key')
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={pincode}&key={GEOCODING_API_KEY}'
    
    try:
        response = requests.get(geocoding_url)
        location_data = response.json()
        
        if location_data['status'] == 'OK':
            location = location_data['results'][0]['geometry']['location']
            lat, lng = location['lat'], location['lng']
            
            # Search for nearby garages using Places API
            PLACES_API_KEY = os.getenv('PLACES_API_KEY', 'your-api-key')
            places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=car_repair&key={PLACES_API_KEY}'
            
            places_response = requests.get(places_url)
            places_data = places_response.json()
            
            garages = []
            for place in places_data.get('results', []):
                garages.append({
                    'name': place['name'],
                    'address': place.get('vicinity', ''),
                    'rating': place.get('rating', 'N/A'),
                    'location': place['geometry']['location'],
                    'place_id': place['place_id']
                })
            
            return jsonify({
                'status': 'success',
                'garages': garages,
                'center': {'lat': lat, 'lng': lng}
            })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    
    return jsonify({
        'status': 'error',
        'message': 'Unable to find garages'
    }), 400

@api.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
@login_required
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if vehicle.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    vehicle.registration = data.get('registration', vehicle.registration)
    vehicle.make = data.get('make', vehicle.make)
    vehicle.model = data.get('model', vehicle.model)
    vehicle.year = data.get('year', vehicle.year)
    vehicle.odometer = data.get('odometer', vehicle.odometer)
    
    db.session.commit()
    return jsonify({'success': True})

@api.route('/vehicles/<int:vehicle_id>/service', methods=['GET'])
@login_required
def get_service_history(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if vehicle.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    service_records = ServiceHistory.query.filter_by(vehicle_id=vehicle_id)\
        .order_by(ServiceHistory.service_date.desc()).all()
    return jsonify([record.to_dict() for record in service_records])

@api.route('/vehicles/<int:vehicle_id>/service', methods=['POST'])
@login_required
def add_service_record(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if vehicle.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    service_record = ServiceHistory(
        vehicle_id=vehicle_id,
        service_date=datetime.strptime(data['service_date'], '%Y-%m-%d'),
        service_type=data['service_type'],
        description=data['description'],
        mileage=int(data['mileage']),
        cost=float(data['cost']) if data.get('cost') else None,
        service_center=data.get('service_center'),
        next_service_date=datetime.strptime(data['next_service_date'], '%Y-%m-%d') if data.get('next_service_date') else None,
        next_service_mileage=int(data['next_service_mileage']) if data.get('next_service_mileage') else None
    )
    
    # Update vehicle's odometer if service mileage is higher
    if service_record.mileage > vehicle.odometer:
        vehicle.odometer = service_record.mileage
    
    # Update vehicle's service schedule
    db.session.add(service_record)
    db.session.commit()
    
    vehicle.update_service_schedule()
    db.session.commit()
    
    return jsonify({'success': True})