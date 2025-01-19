import pandas as pd
import requests
import yfinance as yf
from datetime import datetime
from modules.portfolio_data_manager import StockDataManager
from modules.portfolio_executor import ActionExecutor

class TradingBot:
    def __init__(self, csv_path, broker_simulator=None):
        self.stock_manager = StockDataManager(csv_path)
        self.broker_simulator = broker_simulator

    def run(self):
        """
        Main trading bot logic.
        """
        API_response = 0 #Simulates API response from market trading
        # Step 1: Update current prices
        self.stock_manager.update_current_prices()

        # Step 2: Check buy signals
        buy_signals = self.stock_manager.get_buy_signals()
        print(f"Buy signals: {buy_signals}")

        # Step 3: Execute buy trades
        if buy_signals:
            for signal in buy_signals:
                success = self.broker_simulator.execute_trade(
                    action="buy",
                    ticker=signal['Ticker'],
                    quantity=signal['Quantity'],
                    price=signal['Current Price']
                )
                if success:
                    API_response = 1
                    #print(f"Successfully bought {signal['Quantity']} of {signal['Ticker']}")

        # Step 4: Check sell signals
        sell_signals = self.stock_manager.get_sell_signals()
        print(f"Sell signals: {sell_signals}")

        # Step 5: Execute sell trades
        if sell_signals:
            for signal in sell_signals:
                success = self.broker_simulator.execute_trade(
                    action="sell",
                    ticker=signal['Ticker'],
                    quantity=signal['Quantity'],
                    price=signal['Current Price']
                )
                if success:
                    print(f"Successfully sold {signal['Quantity']} of {signal['Ticker']}")
