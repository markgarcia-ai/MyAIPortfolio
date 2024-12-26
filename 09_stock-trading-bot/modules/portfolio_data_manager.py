import yfinance as yf
import pandas as pd

class StockDataManager:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def update_current_prices(self):
        df = pd.read_csv(self.csv_path)
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

        df.to_csv(self.csv_path, index=False)
        print(f"Updated stock data in {self.csv_path}")