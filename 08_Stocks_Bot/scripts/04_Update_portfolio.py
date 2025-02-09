import os
import time
import pandas as pd
import yfinance as yf
from datetime import datetime  # Ensure datetime is imported

"""
Get the portfolio csv file and update buy at, sell at, stop loss. 
Steps:
1- Read the portfolio csv file and get tickers from there.
2- Calculate the buy at, sell at, stop loss for each ticker.
3- Update the portfolio csv file with the new values.

"""




def function5():
    market_summary_path = "market_summary.csv"
    market_summary = pd.read_csv(market_summary_path)