import os
import time
import pandas as pd
import yfinance as yf
from datetime import datetime  # Ensure datetime is imported

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


def function4():
    market_summary_path = "market_summary.csv"
    market_summary = pd.read_csv(market_summary_path)
    update_market_summary(market_summary_path, market_summary)    