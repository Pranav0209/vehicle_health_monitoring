import joblib
import numpy as np
from pathlib import Path

class FailurePredictionService:
    def __init__(self):
        model_dir = Path(__file__).parent.parent.parent / 'models'
        self.model = joblib.load(model_dir / 'failure_predictor.joblib')
        self.scaler = joblib.load(model_dir / 'failure_scaler.joblib')
        self.label_encoder = joblib.load(model_dir / 'failure_type_encoder.joblib')
    
    def predict_failure(self, air_temp, process_temp, rot_speed, torque, tool_wear):
        # Prepare input features
        features = np.array([[air_temp, process_temp, rot_speed, torque, tool_wear]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Get predicted class
        predicted_class_idx = np.argmax(probabilities)
        predicted_class = self.label_encoder.inverse_transform([predicted_class_idx])[0]
        
        # Create prediction result
        result = {
            'predicted_failure': predicted_class,
            'probability': float(probabilities[predicted_class_idx]),
            'all_probabilities': {
                failure_type: float(prob)
                for failure_type, prob in zip(self.label_encoder.classes_, probabilities)
            }
        }
        
        return result
