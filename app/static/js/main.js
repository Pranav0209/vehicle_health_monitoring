let healthChart;
let currentHealth = 100;

function initializeDashboard() {
    setupHealthChart();
    setupHealthSlider();
    updateMetrics(currentHealth);
    fetchNearbyGarages();
    
    // Update data every 5 seconds
    setInterval(() => {
        if (!document.hidden) {
            updateMetrics(currentHealth);
        }
    }, 5000);
}

function setupHealthChart() {
    const ctx = document.getElementById('healthChart').getContext('2d');
    healthChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Vehicle Health',
                data: [],
                borderColor: '#28a745',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

function setupHealthSlider() {
    const slider = document.getElementById('health-slider');
    slider.addEventListener('input', (e) => {
        currentHealth = parseInt(e.target.value);
        updateMetrics(currentHealth);
    });
}

function updateMetrics(health) {
    // Simulate different vehicle conditions based on health value
    const engineTemp = 80 + (100 - health) * 0.5;
    const oilPressure = 40 - (100 - health) * 0.3;
    const batteryVoltage = 12.6 - (100 - health) * 0.02;
    const fuelLevel = Math.max(0, health);

    // Update metrics display
    document.getElementById('engine-temp').textContent = `${engineTemp.toFixed(1)}°C`;
    document.getElementById('oil-pressure').textContent = `${oilPressure.toFixed(1)} PSI`;
    document.getElementById('battery-voltage').textContent = `${batteryVoltage.toFixed(1)}V`;
    document.getElementById('fuel-level').textContent = `${fuelLevel.toFixed(0)}%`;

    // Update health status
    updateHealthStatus(health);
    
    // Update chart
    updateHealthChart(health);
}

function updateHealthStatus(health) {
    const statusElement = document.getElementById('health-status');
    const alertsContainer = document.getElementById('alerts-container');
    let status, alertClass, alerts = [];

    if (health >= 80) {
        status = 'Healthy';
        alertClass = 'alert-success';
    } else if (health >= 60) {
        status = 'Fair';
        alertClass = 'alert-warning';
        alerts.push('Maintenance recommended soon');
    } else if (health >= 40) {
        status = 'Poor';
        alertClass = 'alert-warning';
        alerts.push('Immediate maintenance required');
        alerts.push('Performance may be affected');
    } else {
        status = 'Critical';
        alertClass = 'alert-danger';
        alerts.push('WARNING: Critical condition detected');
        alerts.push('Immediate service required');
        alerts.push('Unsafe to drive');
    }

    statusElement.className = `alert ${alertClass}`;
    statusElement.textContent = `Vehicle Status: ${status}`;

    // Update alerts
    alertsContainer.innerHTML = alerts
        .map(alert => `<div class="alert ${alertClass}">${alert}</div>`)
        .join('');

    // If health is critical, fetch nearby garages
    if (health < 40) {
        fetchNearbyGarages();
    }
}

function updateHealthChart(health) {
    const now = new Date();
    const label = now.toLocaleTimeString();

    healthChart.data.labels.push(label);
    healthChart.data.datasets[0].data.push(health);

    // Keep only last 10 data points
    if (healthChart.data.labels.length > 10) {
        healthChart.data.labels.shift();
        healthChart.data.datasets[0].data.shift();
    }

    healthChart.update();
}

function fetchNearbyGarages() {
    // Simulate getting user's location
    const mockLat = 37.7749;
    const mockLon = -122.4194;

    fetch(`/api/nearby-garages?lat=${mockLat}&lon=${mockLon}`)
        .then(response => response.json())
        .then(data => {
            const garagesContainer = document.getElementById('garages-container');
            garagesContainer.innerHTML = data.garages
                .map(garage => `
                    <div class="col-md-4">
                        <div class="garage-card">
                            <h5>${garage.name}</h5>
                            <p>Distance: ${garage.distance}</p>
                            <p class="rating">
                                ${'★'.repeat(Math.floor(garage.rating))}
                                ${'☆'.repeat(5 - Math.floor(garage.rating))}
                                ${garage.rating}
                            </p>
                        </div>
                    </div>
                `)
                .join('');
        })
        .catch(error => console.error('Error fetching garages:', error));
}
