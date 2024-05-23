// home_chart.js

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

document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_job_quantities')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('jobQuantityChart').getContext('2d');

            new Chart(ctx, {
                type: 'pie',  // Change chart type to 'pie'
                data: {
                    labels: data.vehicleTypes,
                    datasets: [{
                        label: 'Jumlah',  // Label for the dataset (without color association)
                        data: data.quantities,
                        borderWidth: 1
                    }]
                },
                options: {
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


// Modify home_chart.js to include a new chart for job costs and profits
document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_job_costs_profits')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('jobCostsProfitsChart').getContext('2d');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.jobTypes,
                    datasets: [{
                        label: 'Kos per Unit(Purata)',
                        backgroundColor: 'rgba(255, 99, 132, 0.8)',
                        data: data.costsPerUnit
                    },
                    {
                        label: 'Untung per Unit(Purata)',
                        backgroundColor: 'rgba(54, 162, 235, 0.8)',
                        data: data.profitsPerUnit
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                color: 'black'
                            }
                        },
                        x: {
                            ticks: {
                                color: 'black'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: true,
                            labels: {
                                color: 'black'
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: (tooltipItem) => {
                                    return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toFixed(2);
                                }
                            }
                        }
                    }
                }
            });
            
        })
        .catch(error => console.error('Error fetching job costs and profits:', error));
});

document.addEventListener('DOMContentLoaded', function() {
    let chart; // Chart instance variable

    // Fetch job profitability trends data from server
    fetch('/get_job_profitability_trends')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('jobProfitabilityTrendChart').getContext('2d');

            // Initialize the chart with full dataset
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.jobDates,
                    datasets: [{
                        label: 'Keuntungan (RM)',
                        borderColor: 'rgba(255, 159, 64, 0.6)',
                        data: data.profits
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            display: true,
                            labels: {
                                color: 'black'
                            }
                        }
                    }
                }
            });

            // Set initial label for the date range slider
            const maxDataPoints = data.jobDates.length;
            document.getElementById('dateRangeLabel').textContent = `(${maxDataPoints} data points)`;

            // Update chart based on slider input
            const slider = document.getElementById('dateRangeSlider');
            const label = document.getElementById('dateRangeLabel');

            slider.oninput = function() {
                const rangeValue = parseInt(this.value);
                const maxIndex = Math.floor((rangeValue / 500) * maxDataPoints);

                // Update chart labels and data based on selected date range
                chart.data.labels = data.jobDates.slice(0, maxIndex);
                chart.data.datasets[0].data = data.profits.slice(0, maxIndex);
                chart.update();

                // Update the label to show the number of data points displayed
                label.textContent = `(${maxIndex} data points)`;
            };
        })
        .catch(error => console.error('Error fetching job profitability trends:', error));
});

document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_aftersales_data')
        .then(response => response.json())
        .then(data => {
            const chassisTypes = data.map(item => item.chassisType); // Extract chassis types
            const chassisTypeCounts = {}; // Object to store counts of each chassis type

            // Count occurrences of each chassis type
            chassisTypes.forEach(type => {
                if (chassisTypeCounts[type]) {
                    chassisTypeCounts[type]++;
                } else {
                    chassisTypeCounts[type] = 1;
                }
            });

            // Prepare data in the format required for bar chart
            const labels = Object.keys(chassisTypeCounts);
            const dataCounts = Object.values(chassisTypeCounts);
            const backgroundColors = generateRandomColors(labels.length);

            const barChartData = {
                labels: labels,
                datasets: [{
                    label: '',
                    data: dataCounts,
                    backgroundColor: backgroundColors
                }]
            };

            // Render bar chart
            const ctx = document.getElementById('aftersalesBarChart').getContext('2d');
            const myChart = new Chart(ctx, {
                type: 'bar',
                data: barChartData,
                options: {
                    plugins: {
                        legend: {
                            display: false,
                            position: 'bottom'
                        }
                    },
                    tooltips: {
                        callbacks: {
                            label: function(tooltipItem) {
                                const chassisType = labels[tooltipItem.index];
                                const count = dataCounts[tooltipItem.index];
                                return `${chassisType}: ${count}`; // Display chassisType: count
                            }
                        }
                    }
                }
            });

        })
        .catch(error => console.error('Error fetching aftersales data:', error));
});
