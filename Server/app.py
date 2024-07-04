from flask import Flask, render_template, request, jsonify
from classes.graph import GraphManager
import yfinance as yf
import pandas as pd

app = Flask(__name__)
graph_manager = GraphManager('data.json')

def get_sp500_stocks():
    # Download S&P 500 data
    sp500 = yf.Ticker("^GSPC")
    return sp500

def get_best_stocks():
    # Dummy data for best stocks - Replace with actual logic to determine best stocks
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    stock_data = yf.download(tickers, period="5d")
    stock_data = stock_data['Adj Close'].pct_change().iloc[-1]
    best_stocks = stock_data.sort_values(ascending=False).head(3)
    return best_stocks.index.tolist()

@app.route('/add', methods=['POST'])
def add_data():
    new_data = request.json
    graph_manager.add_data(new_data)
    return jsonify(success=True)

@app.route('/')
def index():
    data = graph_manager.get_data()
    return render_template('index.html', data=data)

@app.route('/invest', methods=['POST'])
def invest():
    budget = float(request.form['budget'])
    best_stocks = get_best_stocks()

    investment_options = []

    # Simple allocation strategy: Equal investment in each stock
    equal_investment = budget / 3
    investments = [{'stock': stock, 'amount': equal_investment} for stock in best_stocks]
    investment_options.append({
        'type': 'Equal Investment',
        'investments': investments
    })

    # Other strategies can be added here
    # Example: Weighted investment based on some criteria (e.g., past performance)
    weighted_investment = budget * pd.Series([0.5, 0.3, 0.2], index=best_stocks)
    investments = [{'stock': stock, 'amount': weighted_investment[stock]} for stock in best_stocks]
    investment_options.append({
        'type': 'Weighted Investment',
        'investments': investments
    })

    return render_template('results.html', options=investment_options)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
