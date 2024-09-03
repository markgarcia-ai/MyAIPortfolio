import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class Investment:
    def __init__(self, ticker, name, quantity):
        self.ticker = ticker
        self.name = name
        self.quantity = quantity
        self.current_price = None
        self.total_value = None

    def fetch_current_price(self, start_date, end_date):
        # Download data from Yahoo Finance
        data = yf.download(self.ticker, start=start_date, end=end_date)['Adj Close']
        if not data.empty:
            self.current_price = data.iloc[-1]
        else:
            self.current_price = 0  # Set to 0 if no data is retrieved

    def calculate_total_value(self):
        if self.current_price is not None:
            self.total_value = self.current_price * self.quantity
        else:
            self.total_value = 0

    def get_summary(self):
        return {
            "Investment Name": self.name,
            "Current Value (GBP)": self.current_price,
            "Quantity": self.quantity,
            "Final Investment Value (GBP)": self.total_value
        }

class Portfolio:
    def __init__(self):
        self.investments = []

    def add_investment(self, ticker, name, quantity):
        investment = Investment(ticker, name, quantity)
        self.investments.append(investment)

    def fetch_prices_and_calculate(self, start_date, end_date):
        for investment in self.investments:
            investment.fetch_current_price(start_date, end_date)
            investment.calculate_total_value()

    def get_portfolio_summary(self):
        summary = []
        for investment in self.investments:
            summary.append(investment.get_summary())
        return pd.DataFrame(summary)

    def calculate_total_investment_value(self):
        total_value = sum(investment.total_value for investment in self.investments)
        return total_value

    def generate_report(self, file_name="investment_summary.csv"):
        summary_df = self.get_portfolio_summary()

        # Add the total investment value as a new row
        total_value = self.calculate_total_investment_value()
        summary_df.loc[len(summary_df)] = ["TOTAL", "", "", total_value]

        # Save to CSV
        summary_df.to_csv(file_name, index=False)
        
        return summary_df


# Define the portfolio and add investments
portfolio = Portfolio()
portfolio.add_investment("TMNLS.L", "TMNLS U.S. Eq Ldrs I/A GBP", 298.944)
portfolio.add_investment("III.L", "3I Group PLC ORD 73 19/22P", 251)
portfolio.add_investment("MOH", "Molina Healthcare Common Stock", 3)
portfolio.add_investment("JPM", "JPM US Select C Acc", 120.289)
portfolio.add_investment("NVCR", "Novocure Limited Ordinary Shares", 20)
portfolio.add_investment("NVDA", "NVIDIA Corp Common Shares", 10)
portfolio.add_investment("BBAI", "BigBearai Holdings Ordinary Shares", 276)
portfolio.add_investment("MSFT", "Microsoft Corp Common Shares", 2)
portfolio.add_investment("ASML", "ASM Holding", 1)

# Calculate the date range (from a week ago to today)
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

# Fetch prices and calculate total values
portfolio.fetch_prices_and_calculate(start_date, end_date)

# Generate the report and print the summary
report_df = portfolio.generate_report()
print(report_df)
