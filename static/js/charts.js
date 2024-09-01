// Pie chart
var pieCtx = document.getElementById('pieChart').getContext('2d');
var pieChart = new Chart(pieCtx, {
    type: 'pie',
    data: {
        labels: ['Depression', 'Anxiety', 'Stress'],
        datasets: [{
            data: [depressionScore, anxietyScore, stressScore],
            backgroundColor: ['#ff6384', '#36a2eb', '#ffcd56'],
            hoverOffset: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
            },
        }
    }
});

// Bar graph
var barCtx = document.getElementById('barGraph').getContext('2d');
var barGraph = new Chart(barCtx, {
    type: 'bar',
    data: {
        labels: ['Depression', 'Anxiety', 'Stress'],
        datasets: [{
            label: 'Score',
            data: [depressionScore, anxietyScore, stressScore],
            backgroundColor: ['#ff6384', '#36a2eb', '#ffcd56'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                display: false,
            },
        }
    }
});
