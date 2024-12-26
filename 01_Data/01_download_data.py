import yfinance as yf
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
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

        # Determine missing ranges
        if existing_end < pd.Timestamp(end_date):
            print(f"Data for {symbol} is missing for dates after {existing_end}. Updating...")
            update_needed = True
            new_start_date = (existing_end + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            new_start_date = start_date
    else:
        print(f"No existing data for {symbol}. Downloading from scratch...")
        new_start_date = start_date

    # Download the missing or full range of data
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


def fetch_sp500_data():
    print("Fetching S&P 500 companies list from Wikipedia...")
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})

    data = []
    print("Processing the table rows...")
    rows = table.find_all('tr')[1:]  # Skip header row
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 8:  # Ensure the row has enough columns
            symbol = cols[0].text.strip()
            company_name = cols[1].text.strip()
            sector = cols[3].text.strip()
            sub_industry = cols[4].text.strip()

            print(f"Fetching data for {symbol} - {company_name}...")
            info = fetch_data_with_retry(symbol)
            if info:
                market_cap = info.get('marketCap', 'N/A')
                previous_close = info.get('previousClose', 'N/A')
                week_high_52 = info.get('fiftyTwoWeekHigh', 'N/A')
                week_low_52 = info.get('fiftyTwoWeekLow', 'N/A')
                avg_price = (week_high_52 + week_low_52) / 2 if week_high_52 != 'N/A' and week_low_52 != 'N/A' else 'N/A'

                data.append([symbol, company_name, sector, sub_industry, market_cap, week_high_52, week_low_52, avg_price, previous_close])
                print(f"Data for {symbol} fetched successfully.")
            else:
                print(f"Skipping {symbol} due to errors.")
                data.append([symbol, company_name, sector, sub_industry, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
            time.sleep(1)  # Throttle requests

    print("Creating DataFrame and saving to CSV...")
    result_df = pd.DataFrame(data, columns=['Symbol', 'Company Name', 'Sector', 'Sub Industry', 'Market Cap', '52-Week High', '52-Week Low', 'Average Price', 'Previous Close'])
    result_df.to_csv('sp500_stocks.csv', index=False)
    print("Data saved to sp500_stocks.csv")


def fetch_nasdaq_data():
    print("Fetching NASDAQ companies list...")
    url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})  # Adjust for the correct table

    data = []
    print("Processing the table rows...")
    rows = table.find_all('tr')[1:]  # Skip header row
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 4:  # Ensure the row has enough columns
            symbol = cols[1].text.strip()  # Symbol is in the second column
            company_name = cols[0].text.strip()  # Company name is in the first column
            sector = cols[2].text.strip() if len(cols) > 2 else 'N/A'

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

    print("Creating DataFrame and saving to CSV...")
    result_df = pd.DataFrame(data, columns=['Symbol', 'Company Name', 'Sector', 'Market Cap', '52-Week High', '52-Week Low', 'Average Price', 'Previous Close'])
    result_df.to_csv('nasdaq_stocks.csv', index=False)
    print("Data saved to nasdaq_stocks.csv")


def fetch_sp_smallcap_600_data():
    print("Fetching S&P SmallCap 600 companies list from Wikipedia...")
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_600_companies'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    data = []
    rows = table.find_all('tr')[1:]  # Skip header row
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 4:
            symbol = cols[0].text.strip()
            company_name = cols[1].text.strip()

            info = fetch_data_with_retry(symbol)
            if info:
                market_cap = info.get('marketCap', 'N/A')
                data.append([symbol, company_name, market_cap])
            else:
                data.append([symbol, company_name, 'N/A'])

    df = pd.DataFrame(data, columns=['Symbol', 'Company Name', 'Market Cap'])
    df.to_csv('sp600_stocks.csv', index=False)


if __name__ == "__main__":
    """
    print("===========STEP 1 : DOWNLOAD STOCKS INFORMATION====================")
    fetch_sp500_data()
    fetch_nasdaq_data()
    

    start_date = '2023-11-23'  # YEAR-MONTH-DAY  
    end_date = '2024-12-10'    # YEAR-MONTH-DAY  

    print("===========STEP 2 : DOWNLOAD SP500 STOCKS DATA====================")
    sp500_csv_file = 'sp500_stocks.csv'
    sp500_symbols = pd.read_csv(sp500_csv_file)['Symbol'].tolist()
    for symbol in sp500_symbols:
        check_and_download_stock_data(symbol, start_date, end_date, 'SP500_data')

    print("===========STEP 3 : DOWNLOAD NASDAQ STOCKS DATA====================")
    nasdaq_csv_file = 'nasdaq_stocks.csv'
    nasdaq_symbols = pd.read_csv(nasdaq_csv_file)['Symbol'].tolist()
    for symbol in nasdaq_symbols:
        check_and_download_stock_data(symbol, start_date, end_date, 'NASDAQ_data')

    """
    start_date = '2023-11-23'  # YEAR-MONTH-DAY  
    end_date = '2024-12-10'    # YEAR-MONTH-DAY 

    fetch_sp_smallcap_600_data()
    print("===========STEP 4 : DOWNLOAD NASDAQ STOCKS DATA====================")
    sp600_csv_file = 'sp600_stocks.csv'
    sp600_symbols = pd.read_csv(sp600_csv_file)['Symbol'].tolist()
    for symbol in sp600_symbols:
        check_and_download_stock_data(symbol, start_date, end_date, 'SP600_data')
