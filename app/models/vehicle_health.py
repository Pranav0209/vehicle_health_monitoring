from app import db
from datetime import datetime
from app.utils.predictive_analytics import PredictiveAnalytics

class VehicleHealth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Engine Parameters
    engine_rpm = db.Column(db.Float, nullable=False)
    oil_pressure = db.Column(db.Float, nullable=False)
    fuel_pressure = db.Column(db.Float, nullable=False)
    coolant_pressure = db.Column(db.Float, nullable=False)
    oil_temperature = db.Column(db.Float, nullable=False)
    coolant_temperature = db.Column(db.Float, nullable=False)
    
    # Maintenance Parameters
    air_temperature = db.Column(db.Float, nullable=False)
    process_temperature = db.Column(db.Float, nullable=False)
    rotation_speed = db.Column(db.Float, nullable=False)
    torque = db.Column(db.Float, nullable=False)
    tool_wear = db.Column(db.Float, nullable=False)
    
    # Analysis Results
    condition = db.Column(db.String(20))
    severity = db.Column(db.String(20))
    failure_type = db.Column(db.String(50))
    maintenance_needed = db.Column(db.Boolean, default=False)
    critical_components = db.Column(db.JSON)

    def __init__(self, vehicle_id, **params):
        self.vehicle_id = vehicle_id
        self.engine_rpm = params.get('engine_rpm', 0)
        self.oil_pressure = params.get('oil_pressure', 0)
        self.fuel_pressure = params.get('fuel_pressure', 0)
        self.coolant_pressure = params.get('coolant_pressure', 0)
        self.oil_temperature = params.get('oil_temperature', 0)
        self.coolant_temperature = params.get('coolant_temperature', 0)
        self.air_temperature = params.get('air_temperature', 298)  # ~25°C
        self.process_temperature = params.get('process_temperature', 308)  # ~35°C
        self.rotation_speed = params.get('rotation_speed', 1500)
        self.torque = params.get('torque', 40)
        self.tool_wear = params.get('tool_wear', 0)
        
        # Run predictive analysis
        self.analyze_health()

    def analyze_health(self):
        """Analyze vehicle health using predictive analytics"""
        analyzer = PredictiveAnalytics()
        
        # Analyze engine condition
        engine_result = analyzer.predict_engine_condition({
            'rpm': self.engine_rpm,
            'oil_pressure': self.oil_pressure,
            'fuel_pressure': self.fuel_pressure,
            'coolant_pressure': self.coolant_pressure,
            'oil_temp': self.oil_temperature,
            'coolant_temp': self.coolant_temperature
        })
        
        # Analyze maintenance needs
        maintenance_result = analyzer.predict_maintenance_needs({
            'air_temp': self.air_temperature,
            'process_temp': self.process_temperature,
            'rotation_speed': self.rotation_speed,
            'torque': self.torque,
            'tool_wear': self.tool_wear
        })
        
        # Update model with analysis results
        self.condition = engine_result['condition']
        self.severity = engine_result['severity']
        self.critical_components = engine_result['components']
        self.failure_type = maintenance_result['failure_type']
        self.maintenance_needed = maintenance_result['maintenance_needed']

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'timestamp': self.timestamp.isoformat(),
            'engine_rpm': self.engine_rpm,
            'oil_pressure': self.oil_pressure,
            'fuel_pressure': self.fuel_pressure,
            'coolant_pressure': self.coolant_pressure,
            'oil_temperature': self.oil_temperature,
            'coolant_temperature': self.coolant_temperature,
            'air_temperature': self.air_temperature,
            'process_temperature': self.process_temperature,
            'rotation_speed': self.rotation_speed,
            'torque': self.torque,
            'tool_wear': self.tool_wear,
            'condition': self.condition,
            'severity': self.severity,
            'failure_type': self.failure_type,
            'maintenance_needed': self.maintenance_needed,
            'critical_components': self.critical_components
        }
