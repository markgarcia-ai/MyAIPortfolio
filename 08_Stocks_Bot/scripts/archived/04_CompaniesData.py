import os
import pandas as pd
import yfinance as yf
import time

# Function to fetch company data using Yahoo Finance
def fetch_company_data(symbol, retries=3, delay=2):
    for attempt in range(retries):
        try:
            # Use yfinance to get ticker data
            ticker = yf.Ticker(symbol)
            
            # Extract the needed data, with a default value of 'Not Available'
            company_name = ticker.info.get('longName', 'Not Available')
            sector = ticker.info.get('sector', 'Not Available')
            industry = ticker.info.get('industry', 'Not Available')
            market_cap = ticker.info.get('marketCap', 'Not Available')
            p_e_ratio = ticker.info.get('trailingPE', 'Not Available')
            p_b_ratio = ticker.info.get('priceToBook', 'Not Available')
            peg_ratio = ticker.info.get('pegRatio', 'Not Available')
            div_yield = ticker.info.get('dividendYield', 'Not Available')
            eps = ticker.info.get('trailingEps', 'Not Available')
            revenue = ticker.info.get('totalRevenue', 'Not Available')
            profit_margin = ticker.info.get('profitMargins', 'Not Available')
            ebitda = ticker.info.get('ebitda', 'Not Available')
            earnings_date = ticker.info.get('nextEarningsDate', 'Not Available')
            stock_market = ticker.info.get('exchange', 'Not Available')  # Fetch the exchange information

            return (company_name, sector, industry, market_cap, p_e_ratio, p_b_ratio, 
                    peg_ratio, div_yield, eps, revenue, profit_margin, ebitda, earnings_date, stock_market)
    
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            time.sleep(delay)
    
    return ('Not Available', 'Not Available', 'Not Available', 'Not Available', 
            'Not Available', 'Not Available', 'Not Available', 'Not Available', 
            'Not Available', 'Not Available', 'Not Available', 'Not Available', 
            'Not Available', 'Not Available')


def calculate_percentage_change(ticker, folder_path, start_date=None, end_date=None):
    """
    Calculate the percentage change for a given stock within a specified time frame.
    """
    file_path = os.path.join(folder_path, f"{ticker}.csv")
    
    if not os.path.exists(file_path):
        print(f"Data file for {ticker} not found in {folder_path}. Skipping.")
        return None
    
    try:
        # Load the stock data
        stock_data = pd.read_csv(file_path)
        
        # Ensure the required columns are present
        if 'Adj Close' not in stock_data.columns or 'Date' not in stock_data.columns:
            print(f"Required columns ('Adj Close', 'Date') not found in {ticker} data. Skipping.")
            return None
        
        # Convert the 'Date' column to datetime and filter by date range
        stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        filtered_data = stock_data[(stock_data['Date'] >= pd.Timestamp(start_date)) & 
                                   (stock_data['Date'] <= pd.Timestamp(end_date))]

        # Check if there is sufficient data for the calculation
        if filtered_data.empty or len(filtered_data) < 2:
            print(f"Not enough data for {ticker} within the specified time frame ({start_date} to {end_date}).")
            return None

        # Extract the first and last adjusted close prices and their dates within the time frame
        first_date = filtered_data['Date'].iloc[0]
        first_value = filtered_data['Adj Close'].iloc[0]
        last_date = filtered_data['Date'].iloc[-1]
        last_value = filtered_data['Adj Close'].iloc[-1]
        
        # Calculate the percentage change
        overall_change = ((last_value - first_value) / first_value) * 100
        
        return {
            'First Date': first_date,
            'First Value': first_value,
            'Last Date': last_date,
            'Last Value': last_value,
            'Percentage Change': overall_change
        }
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        return None

def process_tickers(input_csvs, folder_paths, output_csv, start_date=None, end_date=None):
    """
    Process multiple lists of tickers, calculate percentage change for each, and save results.
    """
    if len(input_csvs) != len(folder_paths):
        raise ValueError("Number of input CSVs and folder paths must match.")
    
    results = []

    for input_csv, folder_path in zip(input_csvs, folder_paths):
        print(f"Processing tickers from {input_csv} using data from {folder_path}...")
        
        # Load the list of tickers from the input CSV
        tickers_df = pd.read_csv(input_csv)
        if tickers_df.empty or tickers_df.columns[0] != 'Ticker':
            print(f"Skipping {input_csv}. Ensure it has a 'Ticker' column as the first column.")
            continue
        
        tickers = tickers_df['Ticker'].tolist()
        
        for ticker in tickers:
            print(f"Calculating percentage change for {ticker}...")
            data = calculate_percentage_change(ticker, folder_path, start_date, end_date)
            
            # Fetch company details
            company_data = fetch_company_data(ticker)
            
            if data is not None:
                results.append({
                    'Ticker': ticker,
                    'First Date': data['First Date'],
                    'First Value': data['First Value'],
                    'Last Date': data['Last Date'],
                    'Last Value': data['Last Value'],
                    'Percentage Change': data['Percentage Change'],
                    'Company Name': company_data[0],
                    'Sector': company_data[1],
                    'Industry': company_data[2],
                    'Market Cap': company_data[3],
                    'P/E Ratio': company_data[4],
                    'P/B Ratio': company_data[5],
                    'PEG Ratio': company_data[6],
                    'Dividend Yield': company_data[7],
                    'EPS': company_data[8],
                    'Revenue': company_data[9],
                    'Profit Margin': company_data[10],
                    'EBITDA': company_data[11],
                    'Earnings Date': company_data[12],
                    'Stock Market': company_data[13],
                    'Source File': input_csv,
                    'Folder Path': folder_path
                })
    
    # Save the results to a new CSV
    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_csv, index=False)
        print(f"Results saved to {output_csv}.")
    else:
        print("No data processed. No results to save.")


def function4():
    print("Function 4 from 04_CompaniesData.py")
    file = 'Output_stocks_combined.csv'
    data_folders = ['SL500_data', 'SP600_data']
    process_csv(file, data_folders)
