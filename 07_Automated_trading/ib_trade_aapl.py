from ib_insync import IB, Stock, MarketOrder

# Connect to Interactive Brokers
def connect_ib(account_id, host='127.0.0.1', port=7497, client_id=1):
    ib = IB()
    try:
        ib.connect(host, port, clientId=client_id)
        print(f"Connected to IB. Account ID: {account_id}")
    except Exception as e:
        print(f"Error connecting to IB: {e}")
        return None
    return ib

# Buy a stock
def buy_stock(ib, symbol, exchange, currency, quantity, account_id):
    try:
        # Define the stock
        stock = Stock(symbol, exchange, currency)
        
        # Request market data to ensure the stock is tradable
        ib.qualifyContracts(stock)
        
        # Create a market order
        order = MarketOrder('BUY', quantity)
        
        # Place the order
        trade = ib.placeOrder(stock, order)
        print(f"Placed order: {trade}")
        ib.sleep(1)  # Wait for order confirmation
        print(f"Order Status: {trade.orderStatus.status}")
        return trade
    except Exception as e:
        print(f"Error buying stock: {e}")
        return None

# Main script
if __name__ == "__main__":
    account_id = "Your_Account_ID"  # Replace with your IB account ID
    host = "127.0.0.1"
    port = 7497  # Use 7497 for paper trading or 7496 for live trading
    client_id = 123  # Any unique ID to identify this connection
    
    symbol = "AAPL"  # Replace with the desired stock symbol
    exchange = "SMART"  # Use 'SMART' for IB's SmartRouting
    currency = "USD"  # Currency of the stock
    quantity = 10  # Number of shares to buy

    # Connect to IB
    ib = connect_ib(account_id, host, port, client_id)
    if ib:
        # Buy the stock
        trade = buy_stock(ib, symbol, exchange, currency, quantity, account_id)
        
        # Disconnect after completing the trade
        ib.disconnect()
