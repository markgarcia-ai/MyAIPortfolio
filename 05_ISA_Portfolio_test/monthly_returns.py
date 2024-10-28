import pandas as pd
import matplotlib.pyplot as plt

# Data: Creating a DataFrame from the provided data
data = {
    'Date': [
        '18/08/2022', '01/01/2023', '31/08/2023', '01/01/2024',
        '01/04/2024', '01/05/2024', '31/08/2024', '10/09/2024',
        '17/09/2024', '21/09/2024', '28/09/2024', '11/10/2024',
        '18/10/2024', '27/10/2024'
    ],
    'Invested': [
        '£149.11', '£1,500.00', '£7,030.00', '£7,430.00', '£14,380.00',
        '£19,230.00', '£15,035.00', '£15,900.00', '£16,908.00', '£16,908.00',
        '£16,908.00', '£17,208.00', '£17,708.00', '£17,708.00'
    ],
    'Value': [
        '£149.11', '£1,497.62', '£7,435.09', '£9,167.94', '£15,890.25',
        '£20,141.79', '£17,073.47', '£16,731.73', '£17,435.00', '£17,637.00',
        '£17,811.00', '£17,961.00', '£19,150.00', '£18,649.00'
    ]
}

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Clean the data
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')  # Convert Date to datetime
df['Invested'] = df['Invested'].replace('[£,]', '', regex=True).astype(float)  # Remove currency symbols and commas
df['Value'] = df['Value'].replace('[£,]', '', regex=True).astype(float)  # Remove currency symbols and commas

# Set the date as the index
df.set_index('Date', inplace=True)

# Display initial DataFrame
print("Initial DataFrame with Invested and Value columns:\n", df)

# Resample data to the end of each month to ensure we have monthly data points
monthly_data = df.resample('M').last()
print("\nData resampled to end of each month:\n", monthly_data)

# Calculate monthly portfolio returns based on portfolio 'Value'
# Monthly return = (Current month value - Previous month value) / Previous month value
monthly_data['Monthly_Return'] = monthly_data['Value'].pct_change()

# Display each step of the monthly return calculation
for i in range(1, len(monthly_data)):
    prev_value = monthly_data['Value'].iloc[i-1]
    current_value = monthly_data['Value'].iloc[i]
    monthly_return = (current_value - prev_value) / prev_value if prev_value != 0 else 0
    print(f"\nMonth {monthly_data.index[i].strftime('%Y-%m')}:")
    print(f"Previous Month Value: {prev_value}")
    print(f"Current Month Value: {current_value}")
    print(f"Monthly Return: {monthly_return:.4f} or {monthly_return * 100:.2f}%")

# Save the data to a CSV file
monthly_data.to_csv('monthly_portfolio_returns.csv', columns=['Value', 'Monthly_Return'])

# Plotting the monthly returns
plt.figure(figsize=(12, 6))
plt.plot(monthly_data.index, monthly_data['Monthly_Return'] * 100, marker='o', linestyle='-', color='b', label='Monthly Return')
plt.title('Monthly Portfolio Returns')
plt.xlabel('Date')
plt.ylabel('Monthly Return (%)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
