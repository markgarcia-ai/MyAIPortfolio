from ib_insync import IB

def check_connection(host='127.0.0.1', port=7497, client_id=1):
    """
    Connects to Interactive Brokers and checks the connection by retrieving account details.
    
    Parameters:
        host (str): The host address for TWS or IB Gateway (default: '127.0.0.1').
        port (int): The port number for TWS or IB Gateway (default: 7497 for paper trading).
        client_id (int): A unique client ID for this connection (default: 1).
    
    Returns:
        None
    """
    ib = IB()
    try:
        # Connect to IB
        ib.connect(host, port, clientId=client_id)
        print("Connected to Interactive Brokers.")
        
        # Fetch account summary
        account_summary = ib.accountSummary()
        print("Account Summary:")
        for row in account_summary:
            print(f"{row.tag}: {row.value} ({row.currency})")
    except Exception as e:
        print(f"Error connecting to IB: {e}")
    finally:
        # Disconnect from IB
        ib.disconnect()
        print("Disconnected from Interactive Brokers.")

# Main execution
if __name__ == "__main__":
    # Update these parameters if needed
    host = "127.0.0.1"  # Default host for TWS/IB Gateway
    port = 7496         # Default port for paper trading (7496 for live trading)
    client_id = 123     # A unique client ID for this script

    check_connection(host, port, client_id)
