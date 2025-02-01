from flask import Blueprint, jsonify, request
import logging

prediction_bp = Blueprint('prediction', __name__)
logger = logging.getLogger(__name__)

@prediction_bp.route('/api/predict-failure', methods=['POST'])
def predict_failure():
    try:
        logger.info("Received prediction request")
        data = request.get_json()
        logger.info(f"Request data: {data}")
        
        # Extract parameters from request
        air_temp = float(data.get('air_temperature'))
        process_temp = float(data.get('process_temperature'))
        rot_speed = float(data.get('rotational_speed'))
        torque = float(data.get('torque'))
        tool_wear = float(data.get('tool_wear'))
        
        logger.info(f"Parameters: air_temp={air_temp}, process_temp={process_temp}, "
                   f"rot_speed={rot_speed}, torque={torque}, tool_wear={tool_wear}")
        
        # Import here to avoid circular import
        from app.services.failure_prediction_service import FailurePredictionService
        failure_predictor = FailurePredictionService()
        
        # Get prediction
        prediction = failure_predictor.predict_failure(
            air_temp, process_temp, rot_speed, torque, tool_wear
        )
        logger.info(f"Prediction result: {prediction}")
        
        return jsonify(prediction)
    
    except Exception as e:
        logger.error(f"Error in predict_failure: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 400
