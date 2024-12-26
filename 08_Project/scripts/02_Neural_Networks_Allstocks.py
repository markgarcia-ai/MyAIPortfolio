"""
Update description
"""
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import os

# Function to calculate short position
def calculate_short_position(csv_file):
    # Load data from the CSV file
    df = pd.read_csv(csv_file)
    
    # Check if the DataFrame is empty
    if df.empty:
        return None, None, None
    
    # Extract the 'Close' prices from the DataFrame
    stock_prices = df['Close'].values.reshape(-1, 1)
    
    # Scale the prices between 0 and 1 for better training
    scaler = MinMaxScaler()
    stock_prices_scaled = scaler.fit_transform(stock_prices)
    
    # Convert the numpy array to a PyTorch tensor
    stock_prices_tensor = torch.tensor(stock_prices_scaled, dtype=torch.float32)
    
    # Define a simple neural network model
    class ShortPositionModel(nn.Module):
        def __init__(self):
            super(ShortPositionModel, self).__init__()
            self.fc1 = nn.Linear(1, 10)  # Input size is 1 (closing price), output size is 10
            self.fc2 = nn.Linear(10, 1)  # Input size is 10, output size is 1
    
        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = self.fc2(x)
            return x
    
    # Instantiate the model
    model = ShortPositionModel()
    
    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Train the model
    num_epochs = 1000
    for epoch in range(num_epochs):
        # Forward pass
        outputs = model(stock_prices_tensor)
        # For simplicity, let's assume the target short position is a constant value (you can replace it with actual target)
        target_short_position = torch.tensor(0.1, dtype=torch.float32)  # Example target short position
        loss = criterion(outputs, target_short_position)
        
        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch+1) % 100 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
    
    # Create a tensor for the last known closing price to predict the next month's short position
    last_known_price = torch.tensor(stock_prices_scaled[-1], dtype=torch.float32).reshape(-1, 1)
    
    # Predict the short position for the next month
    predicted_short_position_scaled = model(last_known_price).item()
    predicted_short_position = scaler.inverse_transform([[predicted_short_position_scaled]])[0][0]
    
    # Get the current stock price
    current_stock_price = df['Close'].iloc[-1]
    
    # Calculate the difference between current stock price and predicted short position
    price_difference = current_stock_price - predicted_short_position
    
    return current_stock_price, predicted_short_position, price_difference


def run_nns(selection,output_file):
    # Directory containing CSV files
    #directory = "stock_data"
    #directory = "portfolio_data"
    directory = selection
    # Output file

    # Iterate over each CSV file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            csv_file = os.path.join(directory, filename)
            stock_name = os.path.splitext(filename)[0]
            
            # Calculate short position for the current CSV file
            current_price, predicted_price, price_difference = calculate_short_position(csv_file)
            
            # Write the results to the output file if the DataFrame is not empty
            if current_price is not None:
                with open(output_file, "a") as f:
                    f.write(f"Symbol: {stock_name}, Current Stock Price: ${current_price:.2f}, Predicted Short Position for Next Month: ${predicted_price:.2f}, Difference: ${price_difference:.2f}\n")
            else:
                print(f"Skipping {filename} because it contains no data.")

def function2():
    print("Function 2 from 02_Neural_Networks_AllStocks.py")
    directory = "SP500_data"
    run_nns(directory,'predicted_short_positions_SP500.txt')
   
    directory = "NASDAQ_data"   
    run_nns(directory,'predicted_short_positions_NASDAQ.txt')    

    directory = "SP600_data"   
    run_nns(directory,'predicted_short_positions_SP600.txt') 

