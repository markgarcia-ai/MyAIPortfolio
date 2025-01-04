import pandas as pd
import requests

class ActionExecutor:
    def __init__(self, csv_path, api_url, api_key):
        self.csv_path = csv_path
        self.api_url = api_url
        self.api_key = api_key
        self.actions = []

    def check_limits(self):
        df = pd.read_csv(self.csv_path)

        for _, row in df.iterrows():
            if row['Price'] <= row['Buy_Limit']:
                self.actions.append({"action": "buy", "ticker": row['Ticker'], "quantity": 10, "price": row['Price']})
            elif row['Price'] >= row['Sell_Limit']:
                self.actions.append({"action": "sell", "ticker": row['Ticker'], "quantity": 10, "price": row['Price']})
    
    def execute_actions(self):
        for action in self.actions:
            response = requests.post(self.api_url, json=action, headers={"Authorization": f"Bearer {self.api_key}"})
            print(f"Executed action: {action}, Response: {response.status_code}")
        return self.actions
    
    def execute_buy(self):
        """
        Need to check balance, how many to buy etc?
        """
        pass

    def execute_sell(self):
        """
        Need to check balance, how many to sell etc?
        """
        pass