import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to scrape S&P 500 tickers, company names, and sectors from Wikipedia
def get_sp500_info():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})
    
    sp500_data = []
    
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        ticker = cells[0].text.strip()
        company_name = cells[1].text.strip()
        sector = cells[3].text.strip()
        sp500_data.append({
            'Ticker': ticker,
            'Company': company_name,
            'Sector': sector
        })
    
    return pd.DataFrame(sp500_data)

# Function to download stock data from Yahoo Finance
def download_stock_data(tickers, start_date, end_date):
    stock_data = {}
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            stock_data[ticker] = data
        except Exception as e:
            print(f"Error downloading data for {ticker}: {e}")
    return stock_data

# Function to calculate percentage profit/loss
def calculate_profit(stock_data):
    profit_data = []
    for ticker, data in stock_data.items():
        try:
            # Get the stock price on March 2000 and March 2023
            price_2000 = data.loc['2000-03-01':'2000-03-31']['Close'].mean()
            price_2023 = data.loc['2023-03-01':'2023-03-31']['Close'].mean()
            
            if pd.notnull(price_2000) and pd.notnull(price_2023):
                # Calculate the percentage profit/loss
                profit_percent = ((price_2023 - price_2000) / price_2000) * 100
                profit_data.append({'Ticker': ticker, 'Profit (%)': profit_percent})
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
    return pd.DataFrame(profit_data)

# Main function
def main():
    # Get the S&P 500 info (tickers, company names, and sectors)
    print("Fetching S&P 500 info...")
    sp500_info = get_sp500_info()
    tickers = sp500_info['Ticker'].tolist()

    # Define the date range
    start_date = '2000-03-01'
    end_date = '2023-03-31'

    # Download stock data
    print("Downloading stock data...")
    stock_data = download_stock_data(tickers, start_date, end_date)

    # Calculate profit for each stock
    print("Calculating profit...")
    profit_df = calculate_profit(stock_data)

    # Merge the profit data with company info (name, sector)
    print("Merging data with company info...")
    final_df = pd.merge(profit_df, sp500_info, on='Ticker')

    # Sort by profit percentage
    final_df = final_df.sort_values(by='Profit (%)', ascending=False)

    # Export the results to Excel
    output_file = 'sp500_stock_profits_2000_to_2023.xlsx'
    print(f"Saving results to {output_file}...")
    final_df.to_excel(output_file, index=False)

    print("Process completed.")

# Run the script
if __name__ == '__main__':
    main()
