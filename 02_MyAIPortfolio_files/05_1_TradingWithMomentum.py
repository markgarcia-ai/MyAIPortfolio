import yfinance as yf
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

#Load Market Data
def download_sp500_data(start_date, end_date, filename='sp500_data.csv'):
    # Load S&P 500 tickers from Wikipedia
    sp500_df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    sp500_tickers = sp500_df['Symbol'].tolist()

    # Initialize an empty DataFrame to store the data
    all_data = pd.DataFrame()

    # Loop through each ticker and download the data
    for ticker in sp500_tickers:
        print(f"Downloading data for {ticker}...")
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        # Check if there's any data for the ticker
        if not data.empty:
            # Reset index and add ticker column
            data.reset_index(inplace=True)
            data['Ticker'] = ticker
            
            # Select only relevant columns and rename them as required
            data = data[['Date', 'Ticker', 'Adj Close']]
            data.rename(columns={'Date': 'date', 'Ticker': 'ticker', 'Adj Close': 'adj_close'}, inplace=True)
            
            # Append to the main DataFrame
            all_data = pd.concat([all_data, data], ignore_index=True)

    # Save the data to CSV
    all_data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

#Plot Market Data
def plot_ticker_from_csv(csv_file, ticker):
    # Load data from CSV
    data = pd.read_csv(csv_file)
    
    # Convert 'date' column to datetime format
    data['date'] = pd.to_datetime(data['date'])
    
    # Filter data for the selected ticker
    ticker_data = data[data['ticker'] == ticker]
    
    # Check if ticker exists in the data
    if ticker_data.empty:
        print(f"No data found for ticker '{ticker}' in {csv_file}")
        return
    
    # Set the 'date' column as the index for resampling
    ticker_data.set_index('date', inplace=True)
    
    # Resample to monthly data, selecting the last observation of each month
    monthly_data = ticker_data['adj_close'].resample('M').last()
    
    # Plot adjusted close price using Matplotlib
    plt.figure(figsize=(10, 6))
    
    # Plot the original daily data
    plt.plot(ticker_data.index, ticker_data['adj_close'], label=f'{ticker} Daily', color='blue')
    
    # Plot the resampled monthly data on top
    plt.plot(monthly_data.index, monthly_data, label=f'{ticker} Monthly (End of Month)', color='red', marker='o')
    
    # Set the title and labels
    plt.title(f'Adjusted Close Price for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Adjusted Close Price')
    plt.legend()
    
    # Set x-axis to show only years
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    # Show the plot
    plt.tight_layout()
    plt.show()

def compute_and_plot_log_returns(csv_file, ticker):
    """
    Computes log returns for a specific ticker's monthly close prices from a CSV file and plots the results.

    Parameters:
    csv_file (str): Path to the CSV file containing price data.
    ticker (str): The ticker symbol to calculate log returns for.

    Returns:
    pd.DataFrame: DataFrame with monthly close prices and log returns for the selected ticker.
    """
    # Load data from CSV
    data = pd.read_csv(csv_file)
    
    # Convert 'date' column to datetime format
    data['date'] = pd.to_datetime(data['date'])
    
    # Filter data for the selected ticker
    ticker_data = data[data['ticker'] == ticker]
    
    # Check if ticker exists in the data
    if ticker_data.empty:
        print(f"No data found for ticker '{ticker}' in {csv_file}")
        return None
    
    # Set the 'date' column as the index for resampling
    ticker_data.set_index('date', inplace=True)
    
    # Resample to monthly data, selecting the last observation of each month for close prices
    monthly_data = ticker_data['adj_close'].resample('M').last()
    
    # Compute log returns: R_t = log(P_t) - log(P_{t-1})
    monthly_data = pd.DataFrame({'monthly_close': monthly_data})
    monthly_data['log_returns'] = np.log(monthly_data['monthly_close']) - np.log(monthly_data['monthly_close'].shift(1))
    
    # Add ticker information as a column
    monthly_data['ticker'] = ticker
    
    # Plot monthly close prices and log returns
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot the monthly close prices
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Monthly Close Price', color='blue')
    ax1.plot(monthly_data.index, monthly_data['monthly_close'], label=f'{ticker} Monthly Close', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis for the log returns
    ax2 = ax1.twinx()
    ax2.set_ylabel('Log Returns', color='red')
    ax2.plot(monthly_data.index, monthly_data['log_returns'], label=f'{ticker} Log Returns', color='red', linestyle='--')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add a title and show the plot
    plt.title(f'Monthly Close Prices and Log Returns for {ticker}')
    fig.tight_layout()  # Adjust layout to prevent overlap
    plt.show()
    
    return monthly_data.reset_index()


if __name__ == "__main__":
    start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    #download_sp500_data(start_date, end_date)
    #plot_ticker_from_csv('sp500_data.csv', 'AAPL')  # Replace 'AAPL' with the ticker you want to plot
    result = compute_and_plot_log_returns('sp500_data.csv', 'AAPL')  # Replace 'AAPL' with your selected ticker
    print(result)




#Resample Adjusted PRices