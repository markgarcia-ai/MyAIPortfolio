$(document).ready(function() {
    const ctx = document.getElementById('myChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(point => point.x),
            datasets: [{
                label: 'Sample Data',
                data: data.map(point => point.y),
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
            }
        }
    });

    $('#dataForm').on('submit', function(event) {
        event.preventDefault();
        const x = $('#x').val();
        const y = $('#y').val();
        const newData = { x: parseFloat(x), y: parseFloat(y) };

        $.ajax({
            url: '/add',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(newData),
            success: function(response) {
                if (response.success) {
                    chart.data.labels.push(newData.x);
                    chart.data.datasets[0].data.push(newData.y);
                    chart.update();
                    $('#x').val('');
                    $('#y').val('');
                }
            }
        });
    });
});
