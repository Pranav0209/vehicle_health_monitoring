import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import os

class PredictiveAnalytics:
    def __init__(self):
        self.engine_data = pd.read_csv('engine_data.csv')
        self.maintenance_data = pd.read_csv('predictive_maintenance.csv')
        
        # Train models
        self.engine_model = self._train_engine_model()
        self.maintenance_model = self._train_maintenance_model()
        
        # Initialize scalers
        self.engine_scaler = StandardScaler()
        self.maintenance_scaler = StandardScaler()
        
        # Fit scalers
        self.engine_scaler.fit(self.engine_data.drop(['Engine Condition'], axis=1))
        self.maintenance_scaler.fit(self.maintenance_data[[
            'Air temperature [K]', 'Process temperature [K]', 
            'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]'
        ]])

    def _train_engine_model(self):
        X = self.engine_data.drop(['Engine Condition'], axis=1)
        y = self.engine_data['Engine Condition']
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model

    def _train_maintenance_model(self):
        X = self.maintenance_data[[
            'Air temperature [K]', 'Process temperature [K]', 
            'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]'
        ]]
        y = self.maintenance_data['Failure Type']
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model

    def predict_engine_condition(self, engine_params):
        """
        Predict engine condition based on current parameters
        
        Args:
            engine_params (dict): Dictionary containing engine parameters
                - rpm: Engine RPM
                - oil_pressure: Lubrication oil pressure
                - fuel_pressure: Fuel pressure
                - coolant_pressure: Coolant pressure
                - oil_temp: Lubrication oil temperature
                - coolant_temp: Coolant temperature
        
        Returns:
            dict: Prediction results with condition and severity
        """
        # Convert parameters to DataFrame
        data = pd.DataFrame([{
            'Engine rpm': engine_params['rpm'],
            'Lub oil pressure': engine_params['oil_pressure'],
            'Fuel pressure': engine_params['fuel_pressure'],
            'Coolant pressure': engine_params['coolant_pressure'],
            'lub oil temp': engine_params['oil_temp'],
            'Coolant temp': engine_params['coolant_temp']
        }])
        
        # Scale the data
        scaled_data = self.engine_scaler.transform(data)
        
        # Get prediction and probabilities
        prediction = self.engine_model.predict(scaled_data)[0]
        probabilities = self.engine_model.predict_proba(scaled_data)[0]
        
        # Determine severity based on probability
        severity = 'high' if probabilities[1] > 0.7 else 'medium' if probabilities[1] > 0.3 else 'low'
        
        return {
            'condition': 'critical' if prediction == 1 else 'normal',
            'severity': severity,
            'probability': float(probabilities[1]),
            'components': self._identify_critical_components(engine_params)
        }

    def predict_maintenance_needs(self, maintenance_params):
        """
        Predict maintenance needs based on current parameters
        
        Args:
            maintenance_params (dict): Dictionary containing maintenance parameters
                - air_temp: Air temperature in Kelvin
                - process_temp: Process temperature in Kelvin
                - rotation_speed: Rotational speed in RPM
                - torque: Torque in Nm
                - tool_wear: Tool wear in minutes
        
        Returns:
            dict: Prediction results with failure type and probability
        """
        # Convert parameters to DataFrame
        data = pd.DataFrame([{
            'Air temperature [K]': maintenance_params['air_temp'],
            'Process temperature [K]': maintenance_params['process_temp'],
            'Rotational speed [rpm]': maintenance_params['rotation_speed'],
            'Torque [Nm]': maintenance_params['torque'],
            'Tool wear [min]': maintenance_params['tool_wear']
        }])
        
        # Scale the data
        scaled_data = self.maintenance_scaler.transform(data)
        
        # Get prediction and probabilities
        failure_type = self.maintenance_model.predict(scaled_data)[0]
        probabilities = self.maintenance_model.predict_proba(scaled_data)[0]
        
        return {
            'failure_type': failure_type,
            'probability': float(max(probabilities)),
            'maintenance_needed': failure_type != 'No Failure'
        }

    def _identify_critical_components(self, params):
        """Identify which components are in critical condition"""
        critical_components = []
        
        # Define thresholds for each parameter
        thresholds = {
            'rpm': {'min': 500, 'max': 2000, 'name': 'Engine RPM'},
            'oil_pressure': {'min': 2.0, 'max': 4.5, 'name': 'Oil Pressure'},
            'fuel_pressure': {'min': 3.0, 'max': 10.0, 'name': 'Fuel System'},
            'coolant_pressure': {'min': 1.0, 'max': 3.5, 'name': 'Cooling System'},
            'oil_temp': {'min': 70, 'max': 85, 'name': 'Oil Temperature'},
            'coolant_temp': {'min': 65, 'max': 90, 'name': 'Engine Temperature'}
        }
        
        for param, value in params.items():
            threshold = thresholds.get(param)
            if threshold:
                if value < threshold['min'] or value > threshold['max']:
                    critical_components.append({
                        'name': threshold['name'],
                        'current': value,
                        'min': threshold['min'],
                        'max': threshold['max']
                    })
        
        return critical_components
