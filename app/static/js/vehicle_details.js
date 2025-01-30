document.addEventListener('DOMContentLoaded', function() {
    // Parameter ranges for sliders
    const parameterRanges = {
        engineRpm: {
            element: 'engineRpmSlider',
            value: 'engineRpmValue',
            min: 0,
            max: 8000,
            unit: ' RPM',
            warning: 6000,
            critical: 7000
        },
        lubOilPressure: {
            element: 'lubOilPressureSlider',
            value: 'lubOilPressureValue',
            min: 0,
            max: 100,
            unit: ' PSI',
            warning: 20,
            critical: 10
        },
        fuelPressure: {
            element: 'fuelPressureSlider',
            value: 'fuelPressureValue',
            min: 0,
            max: 100,
            unit: ' PSI',
            warning: 30,
            critical: 20
        },
        coolantPressure: {
            element: 'coolantPressureSlider',
            value: 'coolantPressureValue',
            min: 0,
            max: 50,
            unit: ' PSI',
            warning: 15,
            critical: 10
        },
        lubOilTemp: {
            element: 'lubOilTempSlider',
            value: 'lubOilTempValue',
            min: 0,
            max: 150,
            unit: '°C',
            warning: 110,
            critical: 130
        },
        coolantTemp: {
            element: 'coolantTempSlider',
            value: 'coolantTempValue',
            min: 0,
            max: 120,
            unit: '°C',
            warning: 95,
            critical: 105
        }
    };

    // Initialize all sliders
    Object.entries(parameterRanges).forEach(([key, config]) => {
        const slider = document.getElementById(config.element);
        if (!slider) return;

        noUiSlider.create(slider, {
            start: [config.min],
            connect: true,
            range: {
                'min': config.min,
                'max': config.max
            }
        });

        // Update value display and check health when slider changes
        slider.noUiSlider.on('update', function(values) {
            const value = Math.round(values[0]);
            const valueElement = document.getElementById(config.value);
            if (valueElement) {
                valueElement.textContent = value + config.unit;
                
                // Update slider color based on value
                const percentage = ((value - config.min) / (config.max - config.min)) * 100;
                if (value <= config.critical) {
                    slider.querySelector('.noUi-connect').style.backgroundColor = '#dc3545'; // danger
                } else if (value <= config.warning) {
                    slider.querySelector('.noUi-connect').style.backgroundColor = '#ffc107'; // warning
                } else {
                    slider.querySelector('.noUi-connect').style.backgroundColor = '#198754'; // success
                }
            }
            updateVehicleHealth();
        });
    });

    // Initialize real-time updates
    const realTimeToggle = document.getElementById('realTimeUpdate');
    let updateInterval;

    realTimeToggle.addEventListener('change', function() {
        if (this.checked) {
            updateInterval = setInterval(simulateParameterChanges, 2000);
        } else {
            clearInterval(updateInterval);
        }
    });

    function simulateParameterChanges() {
        Object.entries(parameterRanges).forEach(([key, config]) => {
            const slider = document.getElementById(config.element);
            if (!slider || !slider.noUiSlider) return;

            const currentValue = parseFloat(slider.noUiSlider.get());
            const change = (Math.random() - 0.5) * (config.max * 0.05); // 5% max change
            const newValue = Math.max(config.min, Math.min(config.max, currentValue + change));
            slider.noUiSlider.set(newValue);
        });
    }

    function updateVehicleHealth() {
        const data = {};
        Object.entries(parameterRanges).forEach(([key, config]) => {
            const slider = document.getElementById(config.element);
            if (slider && slider.noUiSlider) {
                data[key] = parseFloat(slider.noUiSlider.get());
            }
        });

        fetch('/api/vehicle-health/' + vehicleId, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            updateAlerts(result.alerts);
            
            // Show garage modal if there are critical alerts
            if (result.alerts.some(alert => alert.level === 'critical')) {
                findNearbyGarages();
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Handle vehicle edit form submission
    const editVehicleForm = document.getElementById('editVehicleForm');
    if (editVehicleForm) {
        editVehicleForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());
            
            fetch('/api/vehicles/' + vehicleId, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    location.reload();
                } else {
                    alert('Failed to update vehicle details');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Handle service record form submission
    const addServiceForm = document.getElementById('addServiceForm');
    if (addServiceForm) {
        addServiceForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());
            
            fetch('/api/vehicles/' + vehicleId + '/service', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    location.reload();
                } else {
                    alert('Failed to add service record');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Load service history
    function loadServiceHistory() {
        fetch('/api/vehicles/' + vehicleId + '/service')
            .then(response => response.json())
            .then(data => {
                const tbody = document.getElementById('serviceHistoryTable');
                if (!tbody) return;

                tbody.innerHTML = data.map(service => `
                    <tr>
                        <td>${service.service_date}</td>
                        <td>${service.service_type}</td>
                        <td>${service.description}</td>
                        <td>${service.mileage} km</td>
                        <td>${service.cost ? '$' + service.cost.toFixed(2) : '-'}</td>
                        <td>${service.service_center || '-'}</td>
                        <td>${service.next_service_date || '-'}</td>
                    </tr>
                `).join('');
            })
            .catch(error => console.error('Error:', error));
    }

    function updateAlerts(alerts) {
        const alertsContainer = document.getElementById('alertsContainer');
        if (!alertsContainer) return;

        if (!alerts || alerts.length === 0) {
            alertsContainer.innerHTML = '<div class="alert alert-success">No active alerts</div>';
            return;
        }

        alertsContainer.innerHTML = alerts.map(alert => `
            <div class="alert alert-${alert.level === 'critical' ? 'danger' : 'warning'} d-flex align-items-center">
                <i class="fas fa-exclamation-triangle me-2"></i>
                <div>
                    <strong>${alert.component}:</strong> ${alert.message}
                    <div class="small text-muted">Current value: ${alert.value}${alert.unit}</div>
                </div>
            </div>
        `).join('');
    }

    // Load initial service history
    loadServiceHistory();
});
