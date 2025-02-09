class AccountManager:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.portfolio = {}

    def update_balance_and_portfolio(self, actions):
        for action in actions:
            if action['action'] == 'buy':
                self.balance -= action['price'] * action['quantity']
                self.portfolio[action['ticker']] = self.portfolio.get(action['ticker'], 0) + action['quantity']
            elif action['action'] == 'sell':
                self.balance += action['price'] * action['quantity']
                self.portfolio[action['ticker']] -= action['quantity']

        print(f"Updated balance: {self.balance}")
        print(f"Updated portfolio: {self.portfolio}")
        return self.balance, self.portfolio
