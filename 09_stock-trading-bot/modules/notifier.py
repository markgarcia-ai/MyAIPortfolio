import smtplib
import requests
import json
from datetime import datetime
import pandas as pd

class Notifier:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def create_json_from_csv(self):
        json_file_path = 'web_app/data.json'
        try:
            # Read the CSV file
            df = pd.read_csv(self.csv_path)
            # Ensure correct column names and format
            df.columns = [
                "Ticker", "Current Price", "buy at", "Sell at", "Quantity", "API Status", "Balance", "Spare1", "Spare2"
            ]
            # Convert the DataFrame to a JSON-friendly format
            data = {
                "last_updated": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "stocks": df.to_dict(orient='records')
            }

            # Save the JSON data locally for the web app
            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            print(f"JSON file successfully created at {json_file_path}")

        except Exception as e:
            print(f"Error creating JSON file: {e}")

    @staticmethod
    def send_email(recipient, subject, body):
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('your_email@gmail.com', 'your_password')
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail('your_email@gmail.com', recipient, message)
            print("Email sent!")

    @staticmethod
    def send_json_to_website(data, url):
        response = requests.post(url, json=data)
        print(f"Sent data to website: {response.status_code}")
