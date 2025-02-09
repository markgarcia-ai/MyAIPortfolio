import os
import pandas as pd
from datetime import datetime

def process_stocks(input_csv, tickers_output_csv, top_n_output_csv, tickers=None, top_n=20):
    try:
        print(f"Starting stock processing with input file: {input_csv}")
        
        # Check if the input CSV exists
        if not os.path.exists(input_csv):
            raise FileNotFoundError(f"Input file '{input_csv}' not found.")

        # Read the input CSV
        df = pd.read_csv(input_csv)
        if df.empty:
            raise ValueError(f"Input file '{input_csv}' is empty.")

        print("Input CSV successfully read.")
        print("Available tickers in input CSV:", df['Ticker'].unique())
        
        # Ensure required columns are present
        required_columns = ['Ticker', 'First Value', 'Last Value', 'Percentage Change']
        for column in required_columns:
            if column not in df.columns:
                raise KeyError(f"Input CSV must contain the column '{column}'.")
        
        print("Required columns validated.")

        df['Ticker'] = df['Ticker'].str.upper()  # Ensure uniform casing

        if tickers:
            print(f"Filtering stocks based on provided tickers: {tickers}")
            # Convert tickers string into a list
            ticker_list = [ticker.strip().upper() for ticker in tickers.split(',')]
            selected_df = df[df['Ticker'].isin(ticker_list)]
            print("Tickers found in input CSV:", selected_df['Ticker'].unique())
            output_csv = tickers_output_csv
        else:
            print(f"Selecting top {top_n} stocks based on percentage change.")
            # Sort the stocks by 'Percentage Change' in descending order and select top N
            selected_df = df.sort_values(by='Percentage Change', ascending=False).head(top_n)
            output_csv = top_n_output_csv

        if selected_df.empty:
            raise ValueError("No matching tickers found in the input CSV.")

        print(f"Processing {len(selected_df)} selected stocks.")
        
        # Get the current date for the 'Last update' column
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Calculate 'buy at' and 'stop loss'
        selected_df.loc[:, 'buy at'] = selected_df['Last Value'] + ((2 / 100) * selected_df['Last Value'])
        selected_df.loc[:, 'stop loss'] = selected_df['Last Value'] * 0.8

        # Create a DataFrame for the output format
        output_df = pd.DataFrame({
            'Ticker': selected_df['Ticker'],
            'Current Price': selected_df['Last Value'].round(3),
            'buy at': selected_df['buy at'].round(3),
            'Sell at': (selected_df['Last Value'] * 1.2).round(3),  # Sell at 120% of current price
            'stop loss': selected_df['stop loss'].round(3),
            'Quantity': 0,  # Set Quantity to 0
            'API Status': 'Buy',  # Set API Status to 'Buy'
            'Balance': 0,  # Placeholder balance
            'Bought at': 0.000,
            'Spare 2': 0,  # Placeholder for Spare 2
            'Last update': current_date,  # Add current date
            'Spare 1': 0.000  # Placeholder for Spare 1
        })

        print("Output data frame created.")
        
        # Handle duplicates by comparing tickers
        if os.path.exists(output_csv):
            try:
                print(f"Checking for existing data in {output_csv}.")
                # Read the existing output file
                existing_df = pd.read_csv(output_csv)
                print("Existing tickers in output CSV:", existing_df['Ticker'].unique())
                # Find tickers already present in the output file
                existing_tickers = set(existing_df['Ticker'])
                # Filter out duplicate tickers
                output_df = output_df[~output_df['Ticker'].isin(existing_tickers)]
                # Append only new tickers to the output file
                combined_df = pd.concat([existing_df, output_df], ignore_index=True)
            except Exception as e:
                raise IOError(f"Failed to read or append to the existing output file '{output_csv}': {e}")
        else:
            print(f"Creating new output file: {output_csv}")
            # If the file doesn't exist, create it with the new data
            combined_df = output_df

        # Write to the output CSV file
        combined_df.to_csv(output_csv, index=False, float_format="%.3f")
        print(f"Successfully saved processed data to {output_csv}")

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
    except KeyError as key_error:
        print(f"Error: {key_error}")
    except ValueError as value_error:
        print(f"Error: {value_error}")
    except IOError as io_error:
        print(f"Error: {io_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def function3():
    input_csv = 'combined_percentage_changes.csv'  # Replace with the path to your input file
    tickers_output_csv = 'tickers_portfolio.csv'  # Output file for specific tickers
    top_n_output_csv = 'top_n_portfolio.csv'  # Output file for top N stocks
    tickers = "AMZN, BBAI, LOCL, MS, NVDA, NVCR"  # Replace with the tickers you want to process
    print("Starting function3 execution...")
    process_stocks(input_csv, tickers_output_csv, top_n_output_csv, tickers=tickers)  # Process based on specific tickers
    process_stocks(input_csv, tickers_output_csv, top_n_output_csv, top_n=20)  # Process top 20 by default
    print("Function3 execution completed.")
