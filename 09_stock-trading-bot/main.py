from modules.notifier import Notifier
from modules.portfolio_data_manager import StockDataManager
#from modules.IBKR_Manager import IBKRManager
from modules.portfolio_executor import ActionExecutor
from modules.account_manager import AccountManager
from modules.broker_simulator import BrokerSimulator
from modules.trading_bot import TradingBot

import time


def basic():
    print("Running basic...")
    csv_path = "data/portfolio_2025_01_07.csv"  # Path to the CSV file
    file_path = "data/portfolio_2025_01_07.csv"
    broker_simulator = BrokerSimulator("broker_simulator.json")


    try:
        start_time = time.time()
        elapsed_time = 0
        while elapsed_time < 3600:
            bot = TradingBot(csv_path, broker_simulator)
            bot.run()
            time.sleep(2)
            Account_details = broker_simulator.load_data()
            Notifier_manager = Notifier(file_path,Account_details)
            Notifier_manager.create_json_from_csv()
            time.sleep(3)  # Wait for 10 minutes
            elapsed_time = time.time() - start_time
            print(f"Main running with {elapsed_time}")            
    except Exception as e:
        print(f"An error has occurred {e}")
    finally:
        print("Main has ended.")



def main():
    file_path = "data/portfolio_ikbr.csv"
    IBKR_account = IBKRManager()
    stock_manager = StockDataManager(file_path)
    print(f"{stock_manager}")
    Transactions_manager = ActionExecutor(file_path,"xxx","xxx","xxx")
    Notifier_manager = Notifier(file_path,Account_details)
    Portfolio_manager = AccountManager("BalanceFromIKBR")

    try:
        start_time = time.time()
        elapsed_time = 0
        while elapsed_time < 3600:
#STEP 1 : Load IBKR data for balance, maring, open positions, etc...
            IBKR_account.connect()
            Account_details = IBKR_account.get_account_summary()
#STEP 2: Update CVS Stock data details in the CVS File            
            stock_manager.update_current_prices()
#STEP 3 : Check transactions are required based on stocks prices updates and execute them
            if(stock_manager.check_sell_at_stocks()): Transactions_manager.execute_sell()
            if(stock_manager.check_sell_at_stocks()): Transactions_manager.execute_buy()
#STEP 4 : Update portfolio balance and transactions
            Portfolio_manager.update_balance_and_portfolio()
#STEP 5 : Update json file data and send notification email if required.
            Notifier_manager.create_json_from_csv()
            time.sleep(3)  # Wait for 10 minutes
            elapsed_time = time.time() - start_time
            print(f"Main running with {elapsed_time}")            
    except Exception as e:
        print(f"An error has occurred {e}")
    finally:
        print("Main has ended.")

if __name__ == "__main__":
    #main()
    basic()
