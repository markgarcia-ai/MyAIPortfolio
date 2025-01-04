from ib_insync import IB, util

# Create an IB instance
ib = IB()

# Connect to TWS or IB Gateway
# Default port for TWS is 7497, and for IB Gateway is 4002
try:
    print("Connecting to Interactive Brokers...")
    ib.connect('127.0.0.1', 7497, clientId=1)
    print("Connection successful!")
    
    # Fetch account details
    account_summary = ib.accountSummary()
    print("Account Summary:")
    print(util.df(account_summary))  # Display as a DataFrame
    
    # Disconnect after fetching data
    ib.disconnect()
    print("Disconnected successfully.")
except Exception as e:
    print(f"Error connecting to IBKR: {e}")
