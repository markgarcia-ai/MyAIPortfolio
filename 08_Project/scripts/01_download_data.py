import yfinance as yf
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import time
from requests.exceptions import HTTPError


def fetch_data_with_retry(symbol, retries=3, delay=5):
    """Fetch ticker information with retry mechanism for handling rate limits."""
    for attempt in range(retries):
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info
        except HTTPError as e:
            if e.response.status_code == 429:
                print(f"Rate limit reached for {symbol}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"HTTP error for {symbol}: {e}")
                break
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            break
    return None


def check_and_download_stock_data(symbol, start_date, end_date, data_folder):
    """Check if stock data is already downloaded and complete; if not, download/update."""
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    file_path = os.path.join(data_folder, f"{symbol}.csv")
    update_needed = False

    if os.path.exists(file_path):
        print(f"File exists for {symbol}. Checking data completeness...")
        existing_data = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")
        existing_start = existing_data.index.min()
        existing_end = existing_data.index.max()

        if existing_start <= pd.Timestamp(start_date) and existing_end >= pd.Timestamp(end_date):
            print(f"Data for {symbol} already exists for the full date range ({start_date} to {end_date}). Skipping download.")
            return

        if existing_end < pd.Timestamp(end_date):
            print(f"Data for {symbol} is missing for dates after {existing_end}. Updating...")
            update_needed = True
            new_start_date = (existing_end + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            new_start_date = start_date
    else:
        print(f"No existing data for {symbol}. Downloading from scratch...")
        new_start_date = start_date

    try:
        stock_data = yf.download(symbol, start=new_start_date, end=end_date)
        if not stock_data.empty:
            stock_data.reset_index(inplace=True)
            stock_data = stock_data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]

            if os.path.exists(file_path) and update_needed:
                existing_data = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")
                stock_data.set_index("Date", inplace=True)
                combined_data = pd.concat([existing_data, stock_data]).sort_index().drop_duplicates()
                combined_data.to_csv(file_path)
                print(f"Data for {symbol} updated and saved to {file_path}")
            else:
                stock_data.to_csv(file_path, index=False)
                print(f"Data for {symbol} saved to {file_path}")
        else:
            print(f"No data found for {symbol} in the specified range.")
    except Exception as e:
        print(f"Error downloading data for {symbol}: {e}")
    time.sleep(1)  # Throttle requests


def fetch_market_data(market, url, columns, symbol_col, data_folder):
    """Fetch company and stock data for a given market."""
    print(f"Fetching {market.upper()} companies list...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the correct table
    table = soup.find('table', {'id': 'constituents'})  # Adjust table ID or class as necessary
    if not table:
        print(f"No valid table found for {market.upper()}. Skipping.")
        return

    data = []
    rows = table.find_all('tr')[1:]  # Skip header row
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= len(columns):
            symbol = cols[symbol_col].text.strip()
            company_name = cols[0].text.strip() if len(cols) > 0 else 'N/A'
            sector = cols[3].text.strip() if len(cols) > 3 else 'N/A'

            print(f"Fetching data for {symbol} - {company_name}...")
            info = fetch_data_with_retry(symbol)
            if info:
                market_cap = info.get('marketCap', 'N/A')
                previous_close = info.get('previousClose', 'N/A')
                week_high_52 = info.get('fiftyTwoWeekHigh', 'N/A')
                week_low_52 = info.get('fiftyTwoWeekLow', 'N/A')
                avg_price = (week_high_52 + week_low_52) / 2 if week_high_52 != 'N/A' and week_low_52 != 'N/A' else 'N/A'

                data.append([symbol, company_name, sector, market_cap, week_high_52, week_low_52, avg_price, previous_close])
                print(f"Data for {symbol} fetched successfully.")
            else:
                print(f"Skipping {symbol} due to errors.")
                data.append([symbol, company_name, sector, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
            time.sleep(1)  # Throttle requests

    if not data:
        print(f"No data fetched for {market.upper()}.")
        return

    print(f"Creating DataFrame for {market.upper()} and saving to CSV...")
    result_df = pd.DataFrame(data, columns=['Symbol', 'Company Name', 'Sector', 'Market Cap', '52-Week High', '52-Week Low', 'Average Price', 'Previous Close'])
    result_df.to_csv(f'{market}_stocks.csv', index=False)
    print(f"Data saved to {market}_stocks.csv")

    # Download stock data for all symbols
    symbols = result_df['Symbol'].tolist()
    for symbol in symbols:
        check_and_download_stock_data(symbol, '2023-11-23', '2024-12-20', data_folder)


def function1():
    print("Starting data fetching and processing...")
    markets = {
        'sp500': {
            'enabled': True,
            'url': 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
            'columns': ['Symbol', 'Company Name', 'Sector'],
            'symbol_col': 0,
            'data_folder': 'SP500_data'
        },
        'nasdaq': {
            'enabled': True,
            'url': 'https://en.wikipedia.org/wiki/NASDAQ-100',
            'columns': ['Company Name', 'Symbol', 'Sector'],
            'symbol_col': 1,
            'data_folder': 'NASDAQ_data'
        },
        'sp600': {
            'enabled': True,
            'url': 'https://en.wikipedia.org/wiki/List_of_S%26P_600_companies',
            'columns': ['Symbol', 'Company Name', 'Sector'],
            'symbol_col': 0,
            'data_folder': 'SP600_data'
        },
        'dow_jones': {
            'enabled': True,            
            'url': 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average',
            'columns': ['Company Name', 'Symbol', 'Sector'],
            'symbol_col': 1,
            'data_folder': 'DJIA_data'
        }        
    }

    for market, config in markets.items():
        if config['enabled']:
            fetch_market_data(market, config['url'], config['columns'], config['symbol_col'], config['data_folder'])
        else:
            print(f"Skipping {market.upper()} as it is disabled.")
