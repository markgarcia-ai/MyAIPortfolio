import os
import time
import pandas as pd
import yfinance as yf
from datetime import datetime  # Ensure datetime is imported


def fetch_stock_data_with_delay(symbol, delay=1, log_file=None):
    """
    Fetch stock data for a given symbol with a delay and log messages.

    Parameters:
        symbol (str): The stock symbol to fetch data for.
        delay (int): Time in seconds to wait before making the API call.
        log_file (str): Path to the log file.

    Returns:
        dict: A dictionary containing the stock data.
    """
    time.sleep(delay)  # Introduce delay
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        log_message(f"Fetched data for symbol: {symbol}", log_file)
        return {
            'Symbol': symbol,
            'Company Name': info.get('longName', 'N/A'),
            'Sector': info.get('sector', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            '52-Week High': info.get('fiftyTwoWeekHigh', 'N/A'),
            '52-Week Low': info.get('fiftyTwoWeekLow', 'N/A'),
            'Average Price': info.get('twoHundredDayAverage', 'N/A'),
            'Previous Close': info.get('previousClose', 'N/A')
        }
    except Exception as e:
        error_message = f"Error fetching data for {symbol}: {e}"
        log_message(error_message, log_file)
        return None

def log_message(message, log_file):
    """
    Logs a message to the terminal and a log file.

    Parameters:
        message (str): The message to log.
        log_file (str): Path to the log file.

    Returns:
        None
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_message = f"[{timestamp}] {message}"
    print(formatted_message)
    if log_file:
        with open(log_file, 'a') as f:
            f.write(formatted_message + '\n')

def update_markets_stock_data(folder_path, log_file="update_log.txt"):
    """
    Updates stock data in CSV files within a folder using Yahoo Finance and logs messages.

    Parameters:
        folder_path (str): The path to the folder containing CSV files.
        log_file (str): Path to the log file.

    Returns:
        None
    """
    # List all CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    if not csv_files:
        log_message("No CSV files found in the folder.", log_file)
        return

    updated_files = []
    failed_files = {}

    for csv_file in csv_files:
        log_message(f"Processing file: {csv_file}", log_file)
        file_path = os.path.join(folder_path, csv_file)
        try:
            # Read the CSV file
            df = pd.read_csv(file_path)

            # Ensure the required columns are present
            required_columns = ['Symbol', 'Company Name', 'Sector', 'Market Cap',
                                '52-Week High', '52-Week Low', 'Average Price', 'Previous Close']
            
            # Check for missing columns, case-insensitive
            df_columns_lower = {col.lower(): col for col in df.columns}
            missing_columns = [col for col in required_columns if col.lower() not in df_columns_lower]

            if missing_columns:
                reason = f"Missing required columns: {', '.join(missing_columns)}"
                log_message(f"Skipping {csv_file}: {reason}", log_file)
                failed_files[csv_file] = reason
                continue

            # Rename columns to match expected format for uniformity
            df = df.rename(columns={df_columns_lower[col.lower()]: col for col in required_columns if col.lower() in df_columns_lower})

            log_message(f"Updating data for file: {csv_file}", log_file)

            # Fetch latest data using Yahoo Finance with delay
            updated_data = []
            for symbol in df['Symbol']:
                log_message(f"Fetching data for symbol: {symbol}", log_file)
                stock_data = fetch_stock_data_with_delay(symbol, log_file=log_file)
                if stock_data:
                    updated_data.append(stock_data)

            if not updated_data:
                reason = "Failed to fetch updated data for all symbols."
                log_message(f"Skipping {csv_file}: {reason}", log_file)
                failed_files[csv_file] = reason
                continue

            # Create a DataFrame from the updated data
            updated_df = pd.DataFrame(updated_data)

            # Save the updated data back to the CSV
            updated_df.to_csv(file_path, index=False)
            log_message(f"Successfully updated {csv_file}", log_file)
            updated_files.append(csv_file)

        except FileNotFoundError:
            reason = "File not found."
            log_message(f"Error processing {csv_file}: {reason}", log_file)
            failed_files[csv_file] = reason
        except pd.errors.EmptyDataError:
            reason = "CSV file is empty."
            log_message(f"Error processing {csv_file}: {reason}", log_file)
            failed_files[csv_file] = reason
        except Exception as e:
            reason = f"Unexpected error: {e}"
            log_message(f"Error processing {csv_file}: {reason}", log_file)
            failed_files[csv_file] = reason

    # Summary of updates
    log_message("\nUpdate Summary:", log_file)
    log_message("Successfully updated files:", log_file)
    for file in updated_files:
        log_message(f"- {file}", log_file)

    log_message("\nFailed to update files:", log_file)
    for file, reason in failed_files.items():
        log_message(f"- {file}: {reason}", log_file)

def update_ticker_data(folders):
    """
    Update stock data CSV files with the latest data from Yahoo Finance.

    Parameters:
        folders (list): A list of folder paths containing CSV files.

    Returns:
        None
    """
    for folder in folders:
        # Ensure the folder exists
        if not os.path.isdir(folder):
            print(f"Folder not found: {folder}")
            continue

        # Get all CSV files in the folder
        csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]

        for file in csv_files:
            file_path = os.path.join(folder, file)

            try:
                # Read the CSV file
                df = pd.read_csv(file_path)

                # Ensure the CSV contains a 'Date' column
                if 'Date' not in df.columns:
                    print(f"Skipping file with no 'Date' column: {file_path}")
                    continue

                # Parse the last date from the CSV
                df['Date'] = pd.to_datetime(df['Date'])
                last_date = df['Date'].max()

                # Extract stock ticker from the file name (assuming it's the base name without extension)
                ticker = os.path.splitext(file)[0]

                # Download data from Yahoo Finance
                start_date = (last_date + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
                end_date = datetime.today().strftime('%Y-%m-%d')

                if start_date >= end_date:
                    print(f"Data for {ticker} is already up to date.")
                    continue

                print(f"Downloading data for {ticker} from {start_date} to {end_date}...")
                stock_data = yf.download(ticker, start=start_date, end=end_date)

                if stock_data.empty:
                    print(f"No new data for {ticker}.")
                    continue

                # Reset index and prepare data for appending
                stock_data.reset_index(inplace=True)

                # Align columns with the existing CSV file
                stock_data = stock_data[['Date'] + [col for col in stock_data.columns if col != 'Date']]

                # Append new data to the existing CSV file
                updated_df = pd.concat([df, stock_data], ignore_index=True)
                updated_df.to_csv(file_path, index=False)

                print(f"Successfully updated {ticker} data in {file_path}.")

                # Delay to avoid hitting API rate limits
                time.sleep(2)

            except Exception as e:
                print(f"Error processing file {file_path} for ticker {ticker}: {e}")

def update_market_summary(file_path, market_summary_df, log_file="update_log.txt"):
    """
    Update the market summary file based on stock data updates.

    Parameters:
        file_path (str): Path to the market summary file.
        market_summary_df (pd.DataFrame): The current market summary DataFrame.
        log_file (str): Path to the log file.

    Returns:
        None
    """
    for index, row in market_summary_df.iterrows():
        try:
            market_name = row["Markets"]
            folder = row["Folder"]
            root_file = row["Root file"]

            log_message(f"Processing market: {market_name}", log_file)

            if pd.isna(folder) or not os.path.isdir(folder):
                log_message(f"Skipping {market_name}: Invalid folder path '{folder}'", log_file)
                continue

            # Update data within the folder
            update_stock_data([folder])

            # Update root file counts
            if root_file and os.path.exists(root_file):
                root_df = pd.read_csv(root_file)
                total_stocks = len(root_df)
                market_summary_df.at[index, "Total stocks in root file"] = total_stocks

            # Update CSV counts in folder
            csv_files = [file for file in os.listdir(folder) if file.endswith('.csv')]
            market_summary_df.at[index, "Csv stocks in folder"] = len(csv_files)

            # Update last update timestamp
            market_summary_df.at[index, "Last update"] = datetime.now().strftime("%d/%b/%Y")
            log_message(f"Updated {market_name} summary successfully.", log_file)

        except Exception as e:
            log_message(f"Error processing {market_name}: {e}", log_file)

    # Save the updated market summary file
    market_summary_df.to_csv(file_path, index=False)
    log_message(f"Market summary file saved at {file_path}", log_file)


def function1():
    folder_path = "root_csv_files"  # Replace with your folder path
    #update_markets_stock_data(folder_path)
    folders = ["Market_DJIA_data", "Market_NASDAQ_data","Market_nyse_data","Market_SP500_data","Market_SP600_data"]  # Replace with your folder paths
    update_ticker_data(folders)
    market_summary_path = "market_summary.csv"
    market_summary = pd.read_csv(market_summary_path)
    update_market_summary(market_summary_path, market_summary)    