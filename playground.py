import yfinance as yf

# Define the ticker symbol of the company (e.g., 'AAPL' for Apple)
ticker = 'AAPL'  # Replace 'AAPL' with any other ticker symbol as needed

# Fetch data using yfinance
stock = yf.Ticker(ticker)

# Retrieve the next earnings date
earnings_dates = stock.earnings_dates

if not earnings_dates.empty:
    # Get the most recent upcoming earnings date
    next_earnings_date = earnings_dates.index[0]
    print(f"The next earnings release date for {ticker} is: {next_earnings_date.date()}")
else:
    print(f"No upcoming earnings date found for {ticker}.")
