import yfinance as yf
import pandas as pd

class StockDataManager:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def update_current_prices(self):
        df = pd.read_csv(self.csv_path)
        df['Ticker'] = df['Ticker'].astype(str)
        tickers = list(df['Ticker'].unique())

        stock_data = yf.download(tickers, period="1d", interval="1m", group_by="ticker", auto_adjust=True)

        for index, row in df.iterrows():
            ticker = row['Ticker']
            try:
                if ticker in stock_data and 'Close' in stock_data[ticker].columns:
                    latest_price = stock_data[ticker]['Close'].dropna().iloc[-1]
                    df.at[index, 'Current Price'] = latest_price
                else:
                    df.at[index, 'Current Price'] = None
            except Exception as e:
                print(f"Error updating {ticker}: {e}")
                df.at[index, 'Current Price'] = None

        df.to_csv(self.csv_path, index=False)

    def get_buy_signals(self):
        df = pd.read_csv(self.csv_path)
        buy_signals = df[(df['Current Price'] <= df['buy at']) & (df['API Status'] == 'Buy')]
        return buy_signals[['Ticker', 'Current Price', 'Quantity']].to_dict('records')

    def get_sell_signals(self):
        df = pd.read_csv(self.csv_path)
        sell_signals = df[
            ((df['Current Price'] >= df['Sell at']) | (df['Current Price'] <= df['stop loss'])) &
            (df['API Status'] == 'Buy')
        ]
        return sell_signals[['Ticker', 'Current Price', 'Quantity']].to_dict('records')

