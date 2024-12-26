from modules.notifier import Notifier
from modules.portfolio_data_manager import StockDataManager

import time


def main():
    # Get account data  : Balance, number of stocks, tickers etc.
    # Update csv file based on account data
    # Execute Bot trading.
    file_path = "data/stocks_v2.csv"
    try:
        start_time = time.time()
        elapsed_time = 0
        while elapsed_time < 3600:
            stock_manager = StockDataManager(file_path)
            stock_manager.update_current_prices()


            #Update json file
            Notifier_manager = Notifier(file_path)
            Notifier_manager.create_json_from_csv()
            time.sleep(3)  # Wait for 10 minutes
            elapsed_time = time.time() - start_time
            print(f"Main running with {elapsed_time}")            
    except Exception as e:
        print(f"An error has occurred {e}")

if __name__ == "__main__":
    main()
