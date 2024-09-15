import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Download stock data for the past month
def get_stock_data(ticker):
    data = yf.download(ticker, period='1mo', interval='1d')
    return data

# Calculate MACD (Moving Average Convergence Divergence)
def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()  # Short-term EMA
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()  # Long-term EMA
    macd = short_ema - long_ema
    signal_line = macd.ewm(span=signal_window, adjust=False).mean()  # Signal line
    return macd, signal_line

# Calculate RSI (Relative Strength Index)
def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate Bollinger Bands
def calculate_bollinger_bands(data, window=20):
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()

    upper_band = rolling_mean + (rolling_std * 2)
    lower_band = rolling_mean - (rolling_std * 2)
    return upper_band, rolling_mean, lower_band

# Calculate Fibonacci retracement levels
def calculate_fibonacci_retracement(data):
    max_price = data['Close'].max()
    min_price = data['Close'].min()
    diff = max_price - min_price
    levels = {
        '0%': max_price,
        '23.6%': max_price - 0.236 * diff,
        '38.2%': max_price - 0.382 * diff,
        '50%': max_price - 0.5 * diff,
        '61.8%': max_price - 0.618 * diff,
        '100%': min_price
    }
    return levels

# Plotting the stock data with indicators
def plot_stock_data(data, ticker, save_path):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1, 1]})

    # Plot the closing price along with Bollinger Bands
    upper_band, middle_band, lower_band = calculate_bollinger_bands(data)
    ax1.plot(data['Close'], label=f'{ticker} Closing Price')
    ax1.plot(upper_band, label='Upper Bollinger Band', linestyle='--', color='orange')
    ax1.plot(middle_band, label='Middle Bollinger Band', linestyle='--', color='green')
    ax1.plot(lower_band, label='Lower Bollinger Band', linestyle='--', color='orange')

    # Add Fibonacci retracement levels
    fibonacci_levels = calculate_fibonacci_retracement(data)
    for level, price in fibonacci_levels.items():
        ax1.axhline(price, linestyle='--', label=f'Fibonacci {level} level', alpha=0.5)

    ax1.set_title(f'{ticker} Stock Price with Bollinger Bands and Fibonacci Retracement')
    ax1.legend(loc='best')

    # Plot MACD
    macd, signal_line = calculate_macd(data)
    ax2.plot(macd, label='MACD', color='blue')
    ax2.plot(signal_line, label='Signal Line', color='red')
    ax2.set_title('MACD')
    ax2.legend(loc='best')

    # Plot RSI
    rsi = calculate_rsi(data)
    ax3.plot(rsi, label='RSI', color='purple')
    ax3.axhline(70, linestyle='--', color='red')
    ax3.axhline(30, linestyle='--', color='green')
    ax3.set_title('RSI')
    ax3.legend(loc='best')

    plt.tight_layout()
    
    # Save plot as PNG
    plt.savefig(save_path)
    plt.close()

# Main function to run the script
if __name__ == "__main__":
    tickers = input("Enter three stock tickers separated by commas: ").upper().split(',')
    
    for ticker in tickers:
        ticker = ticker.strip()
        stock_data = get_stock_data(ticker)
        save_path = f"{ticker}_stock_plot.png"
        plot_stock_data(stock_data, ticker, save_path)
        print(f"Plot saved as {save_path}")
