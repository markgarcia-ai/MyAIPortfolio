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
        Main trading bot logic with error handling.
        """
        API_response = 0  # Simulates API response from market trading

        try:
            # Step 1: Update current prices
            self.stock_manager.update_current_prices()
            print(f"Stocks updated at {datetime.now()}")

        except Exception as e:
            print(f"Error updating stock prices: {e}")
            return  # Exit if prices cannot be updated

        try:
            # Step 2: Check buy signals
            buy_signals = self.stock_manager.get_buy_signals()
            if not buy_signals:
                print("No buy signals detected.")
            else:
                print(f"Buy signals: {buy_signals}")

        except Exception as e:
            print(f"Error fetching buy signals: {e}")
            return  # Exit if buy signals cannot be fetched

        try:
            # Step 3: Execute buy trades
            if buy_signals:
                for signal in buy_signals:
                    try:
                        success = self.broker_simulator.execute_trade(
                            action="buy",
                            ticker=signal['Ticker'],
                            quantity=signal['Quantity'],
                            price=signal['Current Price']
                        )
                        if success:
                            API_response = 1
                            print(f"Successfully bought {signal['Quantity']} of {signal['Ticker']}")
                    except Exception as e:
                        print(f"Error executing buy trade for {signal['Ticker']}: {e}")

        except Exception as e:
            print(f"Error processing buy trades: {e}")

        try:
            # Step 4: Check sell signals
            sell_signals = self.stock_manager.get_sell_signals()
            if not sell_signals:
                print("No sell signals detected.")
            else:
                print(f"Sell signals: {sell_signals}")

        except Exception as e:
            print(f"Error fetching sell signals: {e}")
            return  # Exit if sell signals cannot be fetched

        try:
            # Step 5: Execute sell trades
            if sell_signals:
                for signal in sell_signals:
                    try:
                        success = self.broker_simulator.execute_trade(
                            action="sell",
                            ticker=signal['Ticker'],
                            quantity=signal['Quantity'],
                            price=signal['Current Price']
                        )
                        if success:
                            print(f"Successfully sold {signal['Quantity']} of {signal['Ticker']}")
                    except Exception as e:
                        print(f"Error executing sell trade for {signal['Ticker']}: {e}")

        except Exception as e:
            print(f"Error processing sell trades: {e}")