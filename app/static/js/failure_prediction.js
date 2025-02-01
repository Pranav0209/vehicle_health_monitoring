// Function to update the prediction
async function updatePrediction() {
    const parameters = {
        air_temperature: parseFloat(document.getElementById('air-temp-slider').value),
        process_temperature: parseFloat(document.getElementById('process-temp-slider').value),
        rotational_speed: parseFloat(document.getElementById('rot-speed-slider').value),
        torque: parseFloat(document.getElementById('torque-slider').value),
        tool_wear: parseFloat(document.getElementById('tool-wear-slider').value)
    };

    try {
        const response = await fetch('/api/predict-failure', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(parameters)
        });

        const prediction = await response.json();

        // Update prediction display
        const predictionDiv = document.getElementById('prediction-result');
        const probabilityDiv = document.getElementById('prediction-probability');
        
        predictionDiv.textContent = `Predicted Failure Type: ${prediction.predicted_failure}`;
        probabilityDiv.textContent = `Probability: ${(prediction.probability * 100).toFixed(2)}%`;

        // Update probability bars
        const probabilityBarsDiv = document.getElementById('probability-bars');
        probabilityBarsDiv.innerHTML = '';

        Object.entries(prediction.all_probabilities).forEach(([failureType, prob]) => {
            const barContainer = document.createElement('div');
            barContainer.className = 'probability-bar-container';

            const label = document.createElement('div');
            label.className = 'probability-label';
            label.textContent = failureType;

            const bar = document.createElement('div');
            bar.className = 'probability-bar';
            bar.style.width = `${prob * 100}%`;
            bar.style.backgroundColor = failureType === prediction.predicted_failure ? '#4CAF50' : '#ddd';

            const value = document.createElement('div');
            value.className = 'probability-value';
            value.textContent = `${(prob * 100).toFixed(1)}%`;

            barContainer.appendChild(label);
            barContainer.appendChild(bar);
            barContainer.appendChild(value);
            probabilityBarsDiv.appendChild(barContainer);
        });

    } catch (error) {
        console.error('Error:', error);
    }
}

// Add event listeners to all sliders
document.addEventListener('DOMContentLoaded', function() {
    const sliders = [
        'air-temp-slider',
        'process-temp-slider',
        'rot-speed-slider',
        'torque-slider',
        'tool-wear-slider'
    ];

    sliders.forEach(sliderId => {
        const slider = document.getElementById(sliderId);
        if (slider) {
            slider.addEventListener('input', updatePrediction);
        }
    });

    // Initial prediction
    updatePrediction();
});
