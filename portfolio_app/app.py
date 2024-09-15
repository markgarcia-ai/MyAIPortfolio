from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# Load all portfolio data from the JSON files in the portfolio_data directory
def load_all_portfolio_data():
    portfolio_dir = os.path.join(app.root_path, 'portfolio_data')
    portfolio_files = sorted(os.listdir(portfolio_dir))
    all_data = []

    for file in portfolio_files:
        if file.endswith('.json'):
            with open(os.path.join(portfolio_dir, file), 'r') as f:
                data = json.load(f)
                all_data.append(data)
    
    return all_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    portfolio_data = load_all_portfolio_data()
    return jsonify({"portfolio": portfolio_data})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
