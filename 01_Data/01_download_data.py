"""
Update description
"""
import yfinance as yf
import requests
import investpy
import pandas as pd
from datetime import datetime, timedelta
#from ftse_symbols import ftse_100_symbols
from bs4 import BeautifulSoup
import os
#from Neural_Networks_AllStocks import run_nns
#from ConvertToCSV import convert_to_csv

def fetch_sp500_data():
    print("Fetching S&P 500 companies list from Wikipedia...")
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
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
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                market_cap = info.get('marketCap', 'N/A')
                previous_close = info.get('previousClose', 'N/A')
                week_high_52 = info.get('fiftyTwoWeekHigh', 'N/A')
                week_low_52 = info.get('fiftyTwoWeekLow', 'N/A')
                avg_price = (week_high_52 + week_low_52) / 2 if week_high_52 != 'N/A' and week_low_52 != 'N/A' else 'N/A'
                
                data.append([symbol, company_name, sector, sub_industry, market_cap, week_high_52, week_low_52, avg_price, previous_close])
                print(f"Data for {symbol} fetched successfully.")
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                data.append([symbol, company_name, sector, sub_industry, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
    
    print("Creating DataFrame and saving to CSV...")
    result_df = pd.DataFrame(data, columns=['Symbol', 'Company Name', 'Sector', 'Sub Industry', 'Market Cap', '52-Week High', '52-Week Low', 'Average Price', 'Previous Close'])
    result_df.to_csv('sp500_stocks.csv', index=False)
    print("Data saved to sp500_stocks.csv")

def fetch_nasdaq_data():
    print("Fetching NASDAQ companies list...")
    
    # URL for the list of NASDAQ companies (can use a reliable source)
    url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})  # Adjust for the correct table
    
    data = []
    print("Processing the table rows...")
    rows = table.find_all('tr')[1:]  # Skip header row
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 4:  # Ensure the row has enough columns
            symbol = cols[1].text.strip()
            company_name = cols[0].text.strip()
            sector = cols[2].text.strip() if len(cols) > 2 else 'N/A'
            
            print(f"Fetching data for {symbol} - {company_name}...")
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                market_cap = info.get('marketCap', 'N/A')
                previous_close = info.get('previousClose', 'N/A')
                week_high_52 = info.get('fiftyTwoWeekHigh', 'N/A')
                week_low_52 = info.get('fiftyTwoWeekLow', 'N/A')
                avg_price = (week_high_52 + week_low_52) / 2 if week_high_52 != 'N/A' and week_low_52 != 'N/A' else 'N/A'
                
                data.append([symbol, company_name, sector, market_cap, week_high_52, week_low_52, avg_price, previous_close])
                print(f"Data for {symbol} fetched successfully.")
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                data.append([symbol, company_name, sector, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
    
    print("Creating DataFrame and saving to CSV...")
    result_df = pd.DataFrame(data, columns=['Symbol', 'Company Name', 'Sector', 'Market Cap', '52-Week High', '52-Week Low', 'Average Price', 'Previous Close'])
    result_df.to_csv('nasdaq_stocks.csv', index=False)
    print("Data saved to nasdaq_stocks.csv")


def get_symbols_from_csv(csv_file):
    """Read the CSV file and extract the symbols column into a list."""
    df = pd.read_csv(csv_file)
    symbols = df['Symbol'].tolist()
    print(f"Symbols are {symbols}")
    return symbols

def download_stock_data(symbols, start_date, end_date, data_folder):
    """Download stock data for the given symbols and save them to the data folder."""
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    for symbol in symbols:
        print(f"Downloading data for {symbol} from {start_date} to {end_date}...")
        try:
            stock_data = yf.download(symbol, start=start_date, end=end_date)
            if not stock_data.empty:
                file_path = os.path.join(data_folder, f"{symbol}.csv")
                stock_data.to_csv(file_path)
                print(f"Data for {symbol} saved to {file_path}")
            else:
                print(f"No data found for {symbol} in the specified date range.")
        except Exception as e:
            print(f"Error downloading data for {symbol}: {e}")

def get_stock_sentiment(symbol, start_date, end_date):
    try:
        # Download stock data
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        if stock_data.empty:
            return None

        # Calculate moving averages
        stock_data['50_MA'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['200_MA'] = stock_data['Close'].rolling(window=200).mean()

        # Determine the latest moving average values
        latest_data = stock_data.dropna().iloc[-1]  # Drop rows with NA values

        # Generate sentiment based on moving averages
        if latest_data['50_MA'] > latest_data['200_MA']:
            return 'Buy'
        else:
            return 'Sell'
    except Exception as e:
        print(f"Error processing {symbol}: {e}")
        return None

def generate_sp500_sentiments():
    print("Fetching S&P 500 symbols...")
    symbols = get_symbols_from_csv(csv_file)
    sentiments = []

    print("Generating sentiments for each stock...")
    for symbol in symbols:
        print(f"Processing {symbol}...")
        sentiment = get_stock_sentiment(symbol, start_date='2023-01-01', end_date='2024-01-01')
        if sentiment:
            sentiments.append({'Symbol': symbol, 'Sentiment': sentiment})

    print("Saving sentiments to CSV...")
    sentiments_df = pd.DataFrame(sentiments)
    sentiments_df.to_csv('sp500_sentiments.csv', index=False)
    print("Sentiments saved to sp500_sentiments.csv")

def combine_csv_files(stocks_csv, sentiments_csv, output_csv):
    # Load the CSV files into DataFrames
    stocks_df = pd.read_csv(stocks_csv)
    sentiments_df = pd.read_csv(sentiments_csv)

    # Merge the DataFrames on the 'Symbol' column
    combined_df = pd.merge(stocks_df, sentiments_df, on='Symbol', how='left')

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv(output_csv, index=False)
    print(f"Combined data saved to {output_csv}")    

if __name__ == "__main__":
    print("===========STEP 1 : DOWLOAD STOCKS INFORMATION====================")
    fetch_sp500_data()
    fetch_nasdaq_data()
    start_date = '2023-10-29' #YEAR-MONTH-DAY  
    end_date = '2024-10-29' #YEAR-MONTH-DAY  
    print("===========STEP 2 : DOWLOAD SP500 STOCKS DATA====================")
    csv_file = 'sp500_stocks.csv'
    symbols = get_symbols_from_csv(csv_file)   
    download_stock_data(symbols, start_date, end_date,'SP500_data')    
    print("===========STEP 3 : DOWLOAD NASDAQ DATA====================")    
    csv_file = 'nasdaq_stocks.csv'
    symbols = get_symbols_from_csv(csv_file)   
    download_stock_data(symbols, start_date, end_date,'NASDAQ_data')       
    """
    print("===========STEP 3 : DOWLOAD STOCK SENTIMENT======================")    
    generate_sp500_sentiments()
    print("===========STEP 4 : RUN NEURAL NETWORK===========================")
    directory = "data2"   
    run_nns(directory)
    convert_to_csv('predicted_short_positions.txt' ,'output.csv')
    print("===========STEP 5 : CREATE FINAL FILE===========================")
    sentiment_file = 'sp500_sentiments.csv'
    csv_file = 'sp500_stocks.csv'
    combine_csv_files(csv_file,sentiment_file,'final_data.csv')
    combine_csv_files('final_data.csv','output.csv','stock_analysis.csv')    
    """