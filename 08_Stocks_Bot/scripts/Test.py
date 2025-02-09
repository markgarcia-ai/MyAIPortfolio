import pandas as pd
import time
import yfinance as yf
import requests
"""
Script functions: 
load_csv : 
save_csv : 
update_current_prices : 
api_buy_stocks :
api_sell_stocks : 
portfolio_actions : 
process_transactions : 
"""

# Load the CSV file
def load_csv(file_path):
    df = pd.read_csv(file_path)
    
    # Add API Status column if not present
    if 'API Status' not in df.columns:
        df['API Status'] = ""
    
    return df

# Save the CSV file
def save_csv(df, file_path):
    df.to_csv(file_path, index=False)

# Update current prices
def update_current_prices(df):
    print("Update stock prices function===========================================")    
    df['Ticker'] = df['Ticker'].astype(str)  # Ensure Ticker column is string
    tickers = list(df['Ticker'].unique())    # Convert to a list of strings
    print(f"Tickers to update: {tickers}")   # Debugging print to verify tickers

    # Download stock data from yfinance
    stock_data = yf.download(tickers, period="1d", interval="1m", group_by="ticker", auto_adjust=True)
    
    for index, row in df.iterrows():
        ticker = row['Ticker']
        try:
            # Ensure stock_data structure is valid
            if ticker in stock_data and 'Close' in stock_data[ticker].columns:
                latest_price = stock_data[ticker]['Close'].dropna().iloc[-1]
                df.at[index, 'Current Price'] = latest_price
            else:
                print(f"No data found for ticker: {ticker}")
                df.at[index, 'Current Price'] = None
        except Exception as e:
            print(f"Error updating {ticker}: {e}")
            df.at[index, 'Current Price'] = None
    
    return df

# Placeholder for API buy
def api_buy_stock(ticker, shares):
    try:
        print(f"Buying {shares} shares of {ticker}")
        # Simulate API call (replace with actual API logic)
        response = requests.post("https://api.broker.com/buy", json={"ticker": ticker, "shares": shares})
        response.raise_for_status()
        return "Success"
    except requests.RequestException as e:
        print(f"API error while buying {ticker}: {e}")
        return f"Error: {str(e)}"

# Placeholder for API sell
def api_sell_stock(ticker, shares):
    try:
        print(f"Selling {shares} shares of {ticker}")
        # Simulate API call (replace with actual API logic)
        response = requests.post("https://api.broker.com/sell", json={"ticker": ticker, "shares": shares})
        response.raise_for_status()
        return "Success"
    except requests.RequestException as e:
        print(f"API error while selling {ticker}: {e}")
        return f"Error: {str(e)}"

def portfolio_actions(df):
    df['Ticker'] = df['Ticker'].astype(str)
    tickers = list(df['Ticker'].unique())
    for index, row in df.iterrows():
        ticker = row['Ticker']
        buy_at = row['buy at']
        current_price = row['Current Price']
        try:
            if current_price < buy_at:
                print(f"Stock {ticker} shall be bought at {current_price}")
                api_buy_stock(ticker,10)
            else:
                print(f"No action for {ticker} because buy is at {buy_at} and current price is {current_price}")
        except Exception as e:
            print(f"Error while analysing {ticker}")


# Process transactions and update API Status
def process_transactions(df):
    print("Process transactions function===========================================")
    for index, row in df.iterrows():
        ticker = row['Ticker']
        shares = row.get('# shares', 0)  # Default to 0 if not present
        status = row.get('status', "").lower()
        
        if status == 'buy':
            api_status = api_buy_stock(ticker, shares)
        elif status == 'sell':
            api_status = api_sell_stock(ticker, shares)
        else:
            api_status = "No Action"
        
        # Update the API Status column
        df.at[index, 'API Status'] = api_status
        print(f"For {index} the api is {api_status} ")
    
    return df

# Function to execute the logic
def function0():
    file_path = "stocks.csv"
    try:
        start_time = time.time()
        elapsed_time = 0

        while elapsed_time < 3600:  # Run for 1 hour
            print("STEP1 : Loading CSV...")
            df = load_csv(file_path)
            print("CSV loaded successfully.")
            print(df)
            print("STEP 2 : Updating stock table...")
            df = update_current_prices(df)
            print("Stock table updated successfully.")
            print("STEP 3: Check if Portfolio must be updated")
            portfolio_actions(df)
            print("Calling process_transactions...")
            df = process_transactions(df)
            print("process_transactions executed successfully.")

            save_csv(df, file_path)
            print("CSV saved successfully.")

            print("Waiting for 10 minutes...")
            time.sleep(3)  # Wait for 10 minutes
            elapsed_time = time.time() - start_time

    except Exception as e:
        print(f"An error occurred: {e}")
