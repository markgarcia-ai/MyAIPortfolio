// Fetch portfolio data from the backend
fetch('/data')
    .then(response => response.json())
    .then(data => {
        const portfolio = data.portfolio;

        // Extract dates and portfolio values
        const dates = portfolio.map(entry => entry.date);
        const values = portfolio.map(entry => entry.portfolio_value);
        const invested = portfolio.map(entry => entry.portfolio_invested);

        // Create the chart
        const ctx = document.getElementById('portfolioChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'Portfolio Value',
                        data: values,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2,
                        fill: false
                    },
                    {
                        label: 'Invested Amount',
                        data: invested,
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 2,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'month'
                        }
                    }
                }
            }
        });
    });