import alpaca_trade_api as tradeapi
import time

# Define your API keys (Sandbox environment)
API_KEY = "CK308FQX254DUNNBZ39R"
SECRET_KEY = "zw1jzpVMvx481ei2vOzirvXskDNuEcsk6s1D3gb2"
BASE_URL = "https://paper-api.alpaca.markets"

# Initialize Alpaca API client
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version="v2")

# Trading parameters
symbol = "AAPL"
quantity = 1
buy_price = 150.00  # Target buy price
sell_price = 155.00  # Target sell price
stop_loss_price = 145.00  # Stop-loss price

# Check account status
def check_account():
    account = api.get_account()
    print(f"Account status: {account.status}")
    print(f"Cash available: {account.cash}")

# Place a buy order
def place_buy_order():
    try:
        print(f"Placing a buy order for {symbol} at ${buy_price}.")
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type='limit',
            time_in_force='gtc',
            limit_price=buy_price
        )
    except Exception as e:
        print(f"Error placing buy order: {e}")

# Monitor stock price and place sell or stop-loss orders
def monitor_and_trade():
    while True:
        try:
            # Get the latest price data
            barset = api.get_latest_trade(symbol)
            current_price = barset.price

            print(f"Current price of {symbol}: ${current_price}")

            # Check if we own the stock
            positions = api.list_positions()
            owns_stock = any(position.symbol == symbol for position in positions)

            if owns_stock:
                if current_price >= sell_price:
                    print(f"Target reached! Selling {symbol} at ${current_price}.")
                    api.submit_order(
                        symbol=symbol,
                        qty=quantity,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                    )
                    break
                elif current_price <= stop_loss_price:
                    print(f"Stop-loss triggered! Selling {symbol} at ${current_price}.")
                    api.submit_order(
                        symbol=symbol,
                        qty=quantity,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                    )
                    break
            time.sleep(60)  # Check every minute
        except Exception as e:
            print(f"Error during monitoring: {e}")

# Main workflow
def main():
    check_account()
    place_buy_order()
    monitor_and_trade()

if __name__ == "__main__":
    main()
