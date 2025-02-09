from ib_insync import IB, util

class IBKRManager:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        """
        Initialize the IBKRManager.

        Args:
            host (str): IBKR Gateway/Trader Workstation host.
            port (int): Port for IBKR Gateway/Trader Workstation.
            client_id (int): Unique ID for the IBKR client.
        """
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id

    def connect(self):
        """
        Connect to the IBKR Gateway or TWS.
        """
        try:
            self.ib.connect(self.host, self.port, self.client_id)
            print("Connected to Interactive Brokers")
        except Exception as e:
            print(f"Error connecting to IBKR: {e}")

    def get_account_summary(self):
        """
        Retrieve account summary information.

        Returns:
            list: Account summary data as a list of dictionaries.
        """
        try:
            account_summary = self.ib.accountSummary()
            # Convert AccountValue objects to dictionaries
            return [{'account': item.account,
                     'tag': item.tag,
                     'value': item.value,
                     'currency': item.currency}
                    for item in account_summary]
        except Exception as e:
            print(f"Error retrieving account summary: {e}")
            return []

    def get_value_by_tag(self, tag_name):
        """
        Retrieve the value of a specific tag from the account summary.

        Args:
            tag_name (str): The tag name to look for (e.g., 'AccountType').

        Returns:
            str: The value associated with the tag, or None if not found.
        """
        account_summary = self.get_account_summary()
        for entry in account_summary:
            if entry['tag'] == tag_name:
                return entry['value']
        return None

    def get_portfolio(self):
        """
        Retrieve portfolio holdings.

        Returns:
            list: Portfolio data.
        """
        try:
            portfolio = self.ib.portfolio()
            return [pos.contract.symbol for pos in portfolio]
        except Exception as e:
            print(f"Error retrieving portfolio: {e}")
            return []

    def disconnect(self):
        """
        Disconnect from IBKR Gateway or TWS.
        """
        self.ib.disconnect()
        print("Disconnected from Interactive Brokers")