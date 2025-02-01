document.addEventListener('DOMContentLoaded', function() {
    // Get all garage finder buttons
    const garageBtns = document.querySelectorAll('.find-garage-btn');
    const garageModal = document.getElementById('garageModal');
    const garagesList = document.getElementById('garages-list');

    garageBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Show pincode input prompt
            Swal.fire({
                title: 'Enter Your Pincode',
                input: 'text',
                inputAttributes: {
                    autocapitalize: 'off',
                    maxlength: 6,
                    pattern: '[0-9]*'
                },
                showCancelButton: true,
                confirmButtonText: 'Search',
                showLoaderOnConfirm: true,
                preConfirm: (pincode) => {
                    if (!pincode || !/^\d{6}$/.test(pincode)) {
                        Swal.showValidationMessage('Please enter a valid 6-digit pincode');
                        return false;
                    }
                    
                    return fetch('/api/find-garages', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ pincode: pincode })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            throw new Error(data.error);
                        }
                        return data;
                    })
                    .catch(error => {
                        Swal.showValidationMessage(`Request failed: ${error}`);
                    });
                },
                allowOutsideClick: () => !Swal.isLoading()
            }).then((result) => {
                if (result.isConfirmed && result.value) {
                    displayGarages(result.value);
                }
            });
        });
    });

    function displayGarages(data) {
        const { garages, map_html } = data;
        
        // Clear previous content
        garagesList.innerHTML = '';
        
        // Add map
        const mapContainer = document.createElement('div');
        mapContainer.className = 'col-12 mb-4';
        mapContainer.innerHTML = map_html;
        garagesList.appendChild(mapContainer);
        
        // Add garage cards
        garages.forEach(garage => {
            const garageCard = document.createElement('div');
            garageCard.className = 'col-md-6 mb-3';
            garageCard.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${garage.name}</h5>
                        <p class="card-text">
                            ${garage.address ? `<strong>Address:</strong> ${garage.address}<br>` : ''}
                            <strong>Distance:</strong> ${garage.distance}<br>
                            ${garage.phone ? `<strong>Phone:</strong> <a href="tel:${garage.phone}">${garage.phone}</a><br>` : ''}
                            ${garage.website ? `<strong>Website:</strong> <a href="${garage.website}" target="_blank">Visit Website</a>` : ''}
                        </p>
                    </div>
                </div>
            `;
            garagesList.appendChild(garageCard);
        });
        
        // Show modal
        const modal = new bootstrap.Modal(garageModal);
        modal.show();
    }
});
