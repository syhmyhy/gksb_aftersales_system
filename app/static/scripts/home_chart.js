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

// Chart number 1: Combined chart for margin profit, total sales, and total profit every year
document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_combined_job_data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('jobCombinedChart').getContext('2d');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.years,
                    datasets: [{
                        type: 'line',
                        label: 'Margin Keuntungan (%)',
                        borderColor: 'rgba(54, 162, 235, 0.6)',
                        data: data.margin_profit,
                        //tension: 0.1, // Adjust the tension for curve
                        yAxisID: 'y1'
                    }, {
                        type: 'bar',
                        label: 'Jumlah Jualan (RM)',
                        backgroundColor: 'rgba(255, 159, 64, 0.6)',
                        data: data.total_sales,
                        tension: 0.1,
                        yAxisID: 'y2'
                    }, {
                        type: 'bar',
                        label: 'Jumlah Keuntungan (RM)',
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        data: data.total_profit,
                        tension: 0.1,
                        yAxisID: 'y2'
                    }]
                },
                options: {
                    scales: {
                        y1: {
                            type: 'linear',
                            position: 'right',
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Margin Keuntungan (%)'
                            }
                        },
                        y2: {
                            type: 'linear',
                            position: 'left',
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Jumlah (RM)'
                            },
                            grid: {
                                drawOnChartArea: false
                            }
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
            
            // Format numbers as currency
            const formatter = new Intl.NumberFormat('ms-MY', {
                style: 'currency',
                currency: 'MYR'
            });

            // Display overall totals and margin percentage
            document.getElementById('overallTotals').innerHTML = `
                <p>Jumlah Keseluruhan Jualan: ${formatter.format(data.overall_total_sales)}</p>
                <p>Jumlah Keseluruhan Keuntungan: ${formatter.format(data.overall_total_profit)}</p>
                <p>Margin Keuntungan Keseluruhan: ${data.overall_margin_percentage.toFixed(2)}%</p>
            `;
        })
        .catch(error => console.error('Error fetching combined job data:', error));
});

// line chart number 2
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
                    labels: data.years,
                    datasets: [{
                        label: 'Jumlah Jualan (RM)',
                        borderColor: 'rgba(255, 159, 64, 0.6)',
                        data: data.total_sales,
                        tension: 0.3 // Adjust the tension for curve
                    }, {
                        label: 'Jumlah Keuntungan (RM)',
                        borderColor: 'rgba(75, 192, 192, 0.6)',
                        data: data.total_profit,
                        tension: 0.3 // Adjust the tension for curve
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

            // Update the slider max attribute based on the number of data points
            const maxDataPoints = data.years.length;
            const slider = document.getElementById('dateRangeSlider');
            slider.max = maxDataPoints;
            slider.value = maxDataPoints; // Set initial value to max
            document.getElementById('dateRangeLabel').textContent = `(${maxDataPoints} data points)`;

            // Add event listener to update chart based on slider value
            slider.addEventListener('input', function() {
                const range = slider.value;
                chart.data.labels = data.years.slice(0, range);
                chart.data.datasets[0].data = data.total_sales.slice(0, range);
                chart.data.datasets[1].data = data.total_profit.slice(0, range);
                chart.update();
                document.getElementById('dateRangeLabel').textContent = `(${range} data points)`;
            });
        })
        .catch(error => console.error('Error fetching job profitability trends:', error));
});

// pie chart number 3
document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_job_quantities')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('jobQuantityChart').getContext('2d');

            new Chart(ctx, {
                type: 'doughnut',  
                data: {
                    labels: data.vehicleTypes,
                    datasets: [{
                        label: 'Jumlah',  
                        data: data.quantities,
                        backgroundColor: [ // Set custom colors for each data point
                            'rgba(255, 99, 132, 0.8)',  // Red
                            'rgba(54, 162, 235, 0.8)',  // Blue
                            'rgba(255, 206, 86, 0.8)',  // Yellow
                            'rgba(75, 192, 192, 0.8)',  // Green
                            'rgba(153, 102, 255, 0.8)', // Purple
                            'rgba(255, 159, 64, 0.8)',  // Orange
                            'rgba(255, 0, 0, 0.8)',     // Bright Red
                            'rgba(0, 255, 0, 0.8)',     // Bright Green
                            'rgba(0, 0, 255, 0.8)',     // Bright Blue
                            'rgba(128, 0, 128, 0.8)',   // Purple
                            'rgba(255, 165, 0, 0.8)',   // Orange
                            'rgba(0, 128, 128, 0.8)',   // Teal
                            'rgba(128, 128, 0, 0.8)',   // Olive
                            'rgba(128, 0, 0, 0.8)',     // Maroon
                            'rgba(0, 128, 0, 0.8)',     // Green
                            // Add more colors if needed
                        ],
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

// bar chart number 4
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


function confirmLogout() {
    if (confirm("Adakah anda pasti ingin log keluar?")) {
        window.location.href = "{{ url_for('logout') }}";
    }
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'MYR',
        minimumFractionDigits: 2
    }).format(value).replace('MYR', '').trim();
}

async function fetchTopJobs() {
    const response = await fetch('/api/top-jobs');
    const topJobs = await response.json();
    const tableBody = document.getElementById('topJobsTableBody');
    tableBody.innerHTML = ''; // Clear any existing rows

    topJobs.forEach(job => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${job.jobNo}</td>
            <td>${job.title}</td>
            <td>${job.custName}</td>
            <td>${formatCurrency(job.totalProfit)}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Call the function to fetch and display the top jobs when the page loads
window.onload = fetchTopJobs;