document.addEventListener('DOMContentLoaded', function() {
fetch('/get_job_quantities')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('jobQuantityChart').getContext('2d');

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.vehicleTypes,
                datasets: [{
                    label: 'Jenis Kenderaan',  // Label for the dataset (without color association)
                    data: data.quantities,
                    backgroundColor: generateRandomColors(data.quantities.length),  // Generate random colors for each bar
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true  // Start y-axis from zero
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            color: 'black'  // Set legend label color (if needed)
                        }
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error fetching job quantities:', error));
});

// Function to generate random colors based on the number of data points
function generateRandomColors(numColors) {
    const colors = [];
    for (let i = 0; i < numColors; i++) {
        const color = `rgba(${getRandomValue()}, ${getRandomValue()}, ${getRandomValue()}, 0.6)`;
        colors.push(color);
    }
    return colors;
}

// Helper function to generate a random value between 0 and 255 for RGB color components
function getRandomValue() {
    return Math.floor(Math.random() * 256);
}
