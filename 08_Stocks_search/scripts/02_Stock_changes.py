import yfinance as yf
import time
import pandas as pd
import os


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
        if tickers_df.empty or tickers_df.columns[0] != 'Symbol':
            print(f"Skipping {input_csv}. Ensure it has a 'Symbol' column as the first column.")
            continue
        
        tickers = tickers_df['Symbol'].tolist()
        
        for ticker in tickers:
            data = calculate_percentage_change(ticker, folder_path, start_date, end_date)
            #print(f"Calculating percentage change between {start_date} to {end_date} for {ticker}...")
            if data is not None:
                results.append({
                    'Ticker': ticker,
                    'First Date': data['First Date'],
                    'First Value': data['First Value'],
                    'Last Date': data['Last Date'],
                    'Last Value': data['Last Value'],
                    'Percentage Change': data['Percentage Change'],
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


def fetch_company_data(symbol, retries=3, delay=2):
    """
    Fetch detailed company data using yfinance.
    Includes additional fields: 52-week high, 52-week low, Dividend Yield, and placeholder for CDP score.
    """
    for attempt in range(retries):
        try:
            ticker = yf.Ticker(symbol)
            # Extract the needed data with a default value of 'Not Available'
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
            stock_market = ticker.info.get('exchange', 'Not Available')
            
            # New fields
            wk52_high = ticker.info.get('fiftyTwoWeekHigh', 'Not Available')
            wk52_low = ticker.info.get('fiftyTwoWeekLow', 'Not Available')
            cdp_score = "Not Available"  # Placeholder for CDP score

            return {
                'Company Name': company_name,
                'Sector': sector,
                'Industry': industry,
                'Market Cap': market_cap,
                'P/E Ratio': p_e_ratio,
                'P/B Ratio': p_b_ratio,
                'PEG Ratio': peg_ratio,
                'Dividend Yield': div_yield,
                'EPS': eps,
                'Revenue': revenue,
                'Profit Margin': profit_margin,
                'EBITDA': ebitda,
                'Earnings Date': earnings_date,
                'Stock Market': stock_market,
                '52-Wk High': wk52_high,
                '52-Wk Low': wk52_low,
                'CDP Score': cdp_score  # Replace with actual data source if available
            }
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            time.sleep(delay)
    
    return {key: 'Not Available' for key in [
        'Company Name', 'Sector', 'Industry', 'Market Cap', 'P/E Ratio',
        'P/B Ratio', 'PEG Ratio', 'Dividend Yield', 'EPS', 'Revenue',
        'Profit Margin', 'EBITDA', 'Earnings Date', 'Stock Market',
        '52-Wk High', '52-Wk Low', 'CDP Score'
    ]}

def filter_output_csv(input_csv, output_csv, min_value, max_value):
    """
    Filter stocks in the output CSV based on value range and positive percentage change.
    Fetch additional company data for filtered stocks.
    """
    try:
        # Load the input CSV
        df = pd.read_csv(input_csv)
        
        # Apply the filters
        filtered_df = df[
            (df['First Value'] >= min_value) &
            (df['Last Value'] <= max_value) &
            (df['Percentage Change'] > 0)
        ]
        
        if filtered_df.empty:
            print("No stocks match the filtering criteria.")
            return
        
        # Fetch company data for each ticker
        enriched_data = []
        for _, row in filtered_df.iterrows():
            ticker = row['Ticker']
            company_data = fetch_company_data(ticker)
            print(f"Fetching company data for {ticker}...")
            
            enriched_row = row.to_dict()
            enriched_row.update(company_data)
            enriched_data.append(enriched_row)
        
        # Convert enriched data to DataFrame and save to output CSV
        enriched_df = pd.DataFrame(enriched_data)
        enriched_df.to_csv(output_csv, index=False)
        print(f"Filtered and enriched results saved to {output_csv}.")
    except Exception as e:
        print(f"Error filtering {input_csv}: {e}")

def ensure_csv_exists(file_path, columns):
    if not os.path.exists(file_path):
        # Create an empty DataFrame with the specified columns
        df = pd.DataFrame(columns=columns)
        # Save the DataFrame to a CSV file
        df.to_csv(file_path, index=False)
        print(f"Created CSV file: {file_path}")
    else:
        print(f"CSV file already exists: {file_path}")


def function2():
    # List of input CSV files and corresponding folder paths
    folder_csv = "root_csv_files/"
    input_csvs = [folder_csv + "dow_jones_stocks.csv",folder_csv + "nyse_tickers.csv",folder_csv + "nasdaq_stocks.csv",folder_csv + "sp500_stocks.csv",folder_csv + "sp600_stocks.csv"]  # Add your input CSVs here
    folder_paths = ["Market_DJIA_data","Market_NASDAQ_data","Market_nyse_data","Market_SP500_data", "Market_SP600_data"]  # Add corresponding folder paths here
    output_csv = "combined_percentage_changes.csv"  # Output CSV file
    filtered_output_csv = "filtered_stocks.csv"  # Final filtered CSV file

    # Specify the time frame
    start_date = "2024-11-20"  # Example start date (YYYY-MM-DD)
    end_date = "2025-01-03"    # Example end date (YYYY-MM-DD)

    # Specify the filtering criteria
    min_value = 1  # Minimum stock value (First Value)
    max_value = 20  # Maximum stock value (Last Value)

    # Process the tickers and calculate percentage changes
    process_tickers(input_csvs, folder_paths, output_csv, start_date, end_date)
    
    # Filter the output CSV based on criteria
    filter_output_csv(output_csv, filtered_output_csv, min_value, max_value)

