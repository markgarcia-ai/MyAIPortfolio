import json
from datetime import datetime

class BrokerSimulator:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = self.load_data()

    def load_data(self):
        """
        Load broker data from the JSON file.
        """
        try:
            with open(self.json_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File '{self.json_file}' not found. Creating a new broker simulation file.")
            default_data = {
                "broker_name": "Simulated Broker",
                "account_id": "12345",
                "balance": 100000.00,
                "trades": []
            }
            self.save_data(default_data)
            return default_data

    def save_data(self, data=None):
        """
        Save broker data to the JSON file.
        """
        if data:
            self.data = data
        with open(self.json_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_balance(self):
        return self.data.get("balance", 0.0)

    def execute_trade(self, action, ticker, quantity, price):
        trade_cost = quantity * price
        if action.lower() == "buy":
            if trade_cost > self.data["balance"]:
                print("Insufficient balance for trade.")
                return False
            self.data["balance"] -= trade_cost
        elif action.lower() == "sell":
            self.data["balance"] += trade_cost
        else:
            print("Invalid trade action.")
            return False

        trade = {
            "action": action.capitalize(),
            "ticker": ticker,
            "quantity": quantity,
            "price": price,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.data["trades"].append(trade)
        self.save_data()
        print(f"Trade executed: {trade}")
        return True

    def get_trades(self):
        return self.data.get("trades", [])