
## Modules Overview

Key file is in data/portfolio_ikbr.csv

To run at the same time the trading bot and website the script run_parallel.py must be run. Two main scripts: <br>
**main.py**
**web_app/app.py**

### 1. `StockDataManager`

**Location:** `modules/stock_data_manager.py`

Handles stock market data retrieval and updates the CSV file.

**Key Methods:**
- `update_stock_data(tickers)`
  - Downloads stock data using `yfinance`.
  - Appends data to the specified CSV file.

### 2. `ActionExecutor`

**Location:** `modules/action_executor.py`

Checks the buy/sell limits from the CSV file and executes actions via an API.

**Key Methods:**
- `check_limits()`
  - Reads the CSV file and determines if any stocks meet buy/sell criteria.
- `execute_actions()`
  - Sends buy/sell requests to the configured API.

### 3. `AccountManager`

**Location:** `modules/account_manager.py`

Updates the account balance and portfolio based on executed actions.

**Key Methods:**
- `update_balance_and_portfolio(actions)`
  - Adjusts the account balance and portfolio holdings based on transactions.

### 4. `Notifier`

**Location:** `modules/notifier.py`

Sends notifications via email or JSON to a website.

**Key Methods:**
- `send_email(recipient, subject, body)`
  - Sends an email with the given details.
- `send_json_to_website(data, url)`
  - Sends JSON data to the specified URL.

### 5. `main.py`

The main script integrates all modules to perform the following steps:
1. Update stock data using `StockDataManager`.
2. Check buy/sell limits and execute actions using `ActionExecutor`.
3. Update balance and portfolio using `AccountManager`.
4. Notify via email or JSON using `Notifier`.

## Requirements

The project requires the following Python libraries:

