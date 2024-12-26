import time
import pandas as pd
import yfinance as yf
import requests

# Load the CSV file
def load_csv(file_path):
    return pd.read_csv(file_path)

# Save the CSV file
def save_csv(df, file_path):
    df.to_csv(file_path, index=False)

# Update current price based on ticker
def update_current_prices(df):
    tickers = df['Ticker'].unique()
    stock_data = yf.download(tickers, period="1d", interval="1m")
    for index, row in df.iterrows():
        ticker = row['Ticker']
        try:
            latest_price = stock_data['Close'][ticker].dropna().iloc[-1]
            df.at[index, 'current price'] = latest_price
        except KeyError:
            print(f"Unable to fetch data for {ticker}")
    return df

# Placeholder for API call to buy stocks
def api_buy_stock(ticker, shares):
    print(f"Buying {shares} shares of {ticker}")
    # Example: requests.post("https://api.broker.com/buy", json={"ticker": ticker, "shares": shares})

# Placeholder for API call to sell stocks
def api_sell_stock(ticker, shares):
    print(f"Selling {shares} shares of {ticker}")
    # Example: requests.post("https://api.broker.com/sell", json={"ticker": ticker, "shares": shares})

# Process the transactions based on status
def process_transactions(df):
    for index, row in df.iterrows():
        ticker = row['Ticker']
        shares = row['# shares']
        status = row['status']
        if status.lower() == 'buy':
            api_buy_stock(ticker, shares)
        elif status.lower() == 'hold':
            api_sell_stock(ticker, shares)

def function6():
    file_path = "Portfolio_draft.csv"
    try:
        start_time = time.time()
        elapsed_time = 0
        while elapsed_time < 3600:  # Run for 1 hour
            df = load_csv(file_path)
            print("Current CSV content:")
            print(df)
            df = update_current_prices(df)
            process_transactions(df)
            save_csv(df, file_path)
            print("Updated and processed transactions. Waiting for 10 minutes...")
            time.sleep(3)  # Wait for 10 minutes
            elapsed_time = time.time() - start_time
    except Exception as e:
        print(f"An error occurred: {e}")