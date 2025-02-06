from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User, Vehicle
from app.models.vehicle_health import VehicleHealth
from app.forms import LoginForm, RegistrationForm, VehicleRegistrationForm
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            name=form.name.data,
            phone=form.phone.data,
            pincode=form.pincode.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/')
@login_required
def dashboard():
    vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', vehicles=vehicles, now=datetime.utcnow())

@main.route('/vehicle/register', methods=['GET', 'POST'])
@login_required
def register_vehicle():
    form = VehicleRegistrationForm()
    if form.validate_on_submit():
        vehicle = Vehicle(
            registration_number=form.registration_number.data,
            make=form.make.data,
            model=form.model.data,
            year=form.year.data,
            fuel_type=form.fuel_type.data,
            current_mileage=form.current_mileage.data,
            service_interval_km=form.service_interval_km.data,
            last_service_date=form.last_service_date.data,
            next_service_date=form.last_service_date.data + timedelta(days=90),
            user_id=current_user.id
        )
        db.session.add(vehicle)
        db.session.commit()
        flash('Vehicle registered successfully!')
        return redirect(url_for('main.dashboard'))
    return render_template('register_vehicle.html', form=form)

@main.route('/vehicle/<int:vehicle_id>')
@login_required
def vehicle_details(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if vehicle.user_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('main.dashboard'))
    return render_template('vehicle_details.html', vehicle=vehicle)

@main.route('/api/vehicle-health/<int:vehicle_id>', methods=['POST'])
@login_required
def update_vehicle_health(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if vehicle.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.json
    health_record = VehicleHealth(
        vehicle_id=vehicle_id,
        **data
    )
    db.session.add(health_record)
    db.session.commit()
    
    prediction = predict_health_status(data)
    return jsonify(prediction)

@main.route('/api/nearby-garages')
@login_required
def find_nearby_garages():
    pincode = request.args.get('pincode', current_user.pincode)
    
    # Use Nominatim to get coordinates from pincode
    geolocator = Nominatim(user_agent="vehicle_health_monitor")
    location = geolocator.geocode(f"{pincode}, India")
    
    if not location:
        return jsonify({'error': 'Invalid pincode'}), 400
    
    # Mock data for nearby garages (in real app, use a garage database or Google Places API)
    nearby_garages = [
        {
            'name': 'AutoCare Service Center',
            'address': f'123 Main Street, {pincode}',
            'distance': '0.5km',
            'rating': 4.5,
            'specialties': ['General Service', 'Engine Repair'],
            'phone': '+91-9876543210'
        },
        {
            'name': 'Premium Car Care',
            'address': f'456 Park Road, {pincode}',
            'distance': '1.2km',
            'rating': 4.2,
            'specialties': ['Luxury Cars', 'Electronic Diagnostics'],
            'phone': '+91-9876543211'
        }
    ]
    
    return jsonify({'garages': nearby_garages})

def predict_health_status(data):
    # Implement prediction logic using kNN
    # This is a simplified version - in production, use the trained model
    alerts = []
    status = 'normal'
    
    # Check engine temperature
    if data.get('engine_temperature', 0) > 100:
        alerts.append('High engine temperature')
        status = 'critical'
    
    # Check oil pressure
    if data.get('oil_pressure', 0) < 20:
        alerts.append('Low oil pressure')
        status = 'critical'
    
    # Check tire pressure
    for tire in ['fl', 'fr', 'rl', 'rr']:
        pressure = data.get(f'tire_pressure_{tire}', 0)
        if pressure < 30:
            alerts.append(f'Low tire pressure ({tire.upper()})')
            status = 'warning'
    
    return {
        'status': status,
        'alerts': alerts,
        'maintenance_required': status == 'critical'
    }

@main.route('/monitor',methods=['GET'])
@login_required
def monitor():
    return render_template("monitor.html")