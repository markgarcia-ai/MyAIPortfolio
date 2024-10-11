import yfinance as yf

try:
    stock = yf.Ticker("ASML")
    info = stock.info
    print(info)
except Exception as e:
    print(f"Failed to retrieve data: {e}")
