import json
import os
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

class InvestmentApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.data_file = 'data.json'
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/add', 'add_entry', self.add_entry, methods=['POST'])
        self.app.add_url_rule('/plot.png', 'plot_png', self.plot_png)
        self.app.add_url_rule('/plot', 'plot_page', self.plot_page)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []

    def save_data(self, data):
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def index(self):
        data = self.load_data()
        return render_template('index.html', data=data)

    def add_entry(self):
        date = request.form['date']
        invested = float(request.form['invested'])
        total_investment = float(request.form['total_investment'])

        data = self.load_data()
        data.append({
            'date': date,
            'invested': invested,
            'total_investment': total_investment
        })
        self.save_data(data)
        
        return redirect(url_for('index'))

    def plot_png(self):
        data = self.load_data()
        dates = [datetime.strptime(entry['date'], '%Y-%m-%d') for entry in data]
        invested = [entry['invested'] for entry in data]
        total_investment = [entry['total_investment'] for entry in data]
        
        plt.figure(figsize=(10, 5))
        plt.plot(dates, invested, label='Invested', marker='o')
        plt.plot(dates, total_investment, label='Total Investment', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('Invested vs Total Investment')
        plt.legend()
        plt.grid(True)
        
        # Save it to a temporary buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    def plot_page(self):
        plot_url = url_for('plot_png')
        return render_template('plot.html', plot_url=plot_url)

    def run(self):
        self.app.run(debug=True)
