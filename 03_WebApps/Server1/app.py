from flask import Flask, render_template
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

class Investment:
    def __init__(self, ticker, name, quantity):
        self.ticker = ticker
        self.name = name
        self.quantity = quantity
        self.current_price = None
        self.total_value = None

    def fetch_current_price(self, start_date, end_date):
        data = yf.download(self.ticker, start=start_date, end=end_date)['Adj Close']
        if not data.empty:
            self.current_price = data.iloc[-1]
        else:
            self.current_price = 0

    def calculate_total_value(self):
        if self.current_price is not None:
            self.total_value = self.current_price * self.quantity
        else:
            self.total_value = 0

    def get_summary(self):
        return {
            "Investment Name": self.name,
            "Current Value (GBP)": round(self.current_price, 2),
            "Quantity": self.quantity,
            "Final Investment Value (GBP)": round(self.total_value, 2)
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
        return round(total_value, 2)


@app.route('/')
def index():
    # Define the portfolio and add investments
    portfolio = Portfolio()
    portfolio.add_investment("III.L", "3I Group PLC ORD 73 19/22P", 50)
    portfolio.add_investment("MOH", "Molina Healthcare Common Stock", 30)
    portfolio.add_investment("JPM", "JPM US Select C Acc", 20)
    portfolio.add_investment("NVCR", "Novocure Limited Ordinary Shares", 10)
    portfolio.add_investment("NVDA", "NVIDIA Corp Common Shares", 40)
    portfolio.add_investment("BBAI", "BigBearai Holdings Ordinary Shares", 200)
    portfolio.add_investment("MSFT", "Microsoft Corp Common Shares", 25)
    portfolio.add_investment("ASML", "ASM Holding", 15)

    # Calculate the date range (from a week ago to today)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    # Fetch prices and calculate total values
    portfolio.fetch_prices_and_calculate(start_date, end_date)

    # Get the summary DataFrame and convert it to HTML
    df = portfolio.get_portfolio_summary()
    total_investment_value = portfolio.calculate_total_investment_value()

    # Add the total row
    df.loc[len(df)] = ["TOTAL", "", "", total_investment_value]

    return render_template('index.html', tables=[df.to_html(classes='data', header="true", index=False)])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
