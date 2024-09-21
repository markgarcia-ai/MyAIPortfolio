import yfinance as yf

# Example: Fetch data for Apple Inc.
ticker = yf.Ticker("AAPL")

# Get company info
info = ticker.info
print("Company Name:", info['longName'])
print("Sector:", info['sector'])
print("Industry:", info['industry'])

# Get valuation metrics
print("P/E Ratio:", info.get('trailingPE'))
print("P/B Ratio:", info.get('priceToBook'))
print("PEG Ratio:", info.get('pegRatio'))

# Get financial statements
income_statement = ticker.financials
balance_sheet = ticker.balance_sheet
cash_flow = ticker.cashflow

# Display financial statements
print("Income Statement:\n", income_statement)
print("Balance Sheet:\n", balance_sheet)
print("Cash Flow Statement:\n", cash_flow)

# Get historical market data
hist = ticker.history(period="1y")
print("Historical Market Data:\n", hist.head())
