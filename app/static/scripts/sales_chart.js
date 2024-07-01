// sales_chart.js

document.addEventListener('DOMContentLoaded', function () {
    // Your existing Chart.js code here
    var salesData = [];
    var profitData = [];
    var marginProfitData = [];
    var salesPersons = [];

    {% for item in sales_data %}
        salesData.push({{ item.total_sales }});
        profitData.push({{ item.total_profit }});
        marginProfitData.push({{ item.margin_profit|round(2) }});
        salesPersons.push('{{ item.salesPerson }}');
    {% endfor %}

    var ctx = document.getElementById('sales-chart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: salesPersons,
            datasets: [{
                type: 'line',
                label: 'Margin Keuntungan (%)',
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(54, 162, 235, 0.6)',
                borderWidth: 2,
                yAxisID: 'y1',
                data: marginProfitData
            }, {
                type: 'bar',
                label: 'Jumlah Jualan (RM)',
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                yAxisID: 'y2',
                data: salesData
            }, {
                type: 'bar',
                label: 'Jumlah Keuntungan (RM)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                yAxisID: 'y2',
                data: profitData
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
});
