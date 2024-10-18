import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from time import sleep

# Function to fetch stock data with retry mechanism
def download_stock_data_with_retry(stock_symbol, start_date, end_date, retries=3, delay=5):
    for attempt in range(retries):
        try:
            stock_data = yf.download(stock_symbol, start=start_date, end=end_date, timeout=20)
            if not stock_data.empty:
                return stock_data
        except Exception as e:
            print(f"Attempt {attempt+1} failed with error: {e}")
        print(f"Retrying in {delay} seconds...")
        sleep(delay)  # Wait for a few seconds before retrying
    print(f"Failed to download data for {stock_symbol} after {retries} attempts.")
    return pd.DataFrame()

# Function to analyze volume impact and save the plot
def analyze_volume(stock_symbol, save_path):
    # Calculate the date range for the latest 30 days
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

    # Download historical data for the given stock over the latest 30 days
    stock_data = download_stock_data_with_retry(stock_symbol, start_date, end_date)

    # Ensure we have sufficient data
    if stock_data.empty:
        print(f"No data found for {stock_symbol}.")
        return

    # Calculate additional metrics
    stock_data['Price Change'] = stock_data['Close'].pct_change() * 100  # percentage change
    stock_data['Price Direction'] = np.where(stock_data['Price Change'] > 0, 'Up', 'Down')

    avg_volume = stock_data['Volume'].mean()

    # Classify volume into high and low volume based on threshold
    high_volume_threshold = avg_volume * 1.5
    low_volume_threshold = avg_volume * 0.5
    stock_data['Volume Level'] = np.where(stock_data['Volume'] > high_volume_threshold, 'High',
                                          np.where(stock_data['Volume'] < low_volume_threshold, 'Low', 'Normal'))

    # --- Plot the data ---
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot the closing price
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Closing Price', color='blue')
    ax1.plot(stock_data.index, stock_data['Close'], color='blue', label='Closing Price')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis for volume
    ax2 = ax1.twinx()
    ax2.set_ylabel('Volume', color='gray')
    ax2.bar(stock_data.index, stock_data['Volume'], color='gray', alpha=0.3, label='Volume')
    ax2.tick_params(axis='y', labelcolor='gray')

    fig.tight_layout()
    plt.title(f"Stock Volume and Price Analysis for {stock_symbol.upper()} (Last 30 Days)")

    # Save the plot as a PNG file
    plt.savefig(save_path)
    plt.close()

    print(f"Plot saved as {save_path}")

# Main function to analyze multiple tickers and save each plot
if __name__ == "__main__":
    tickers = input("Enter three stock tickers separated by commas: ").upper().split(',')

    for ticker in tickers:
        ticker = ticker.strip()
        save_path = f"{ticker}_volume_analysis.png"
        analyze_volume(ticker, save_path)
        print(f"Analysis completed for {ticker}")
