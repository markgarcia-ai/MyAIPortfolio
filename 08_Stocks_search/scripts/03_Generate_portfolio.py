import pandas as pd
from datetime import datetime
import os

def process_top_20_stocks(input_csv, output_csv):
    try:
        # Check if the input CSV exists
        if not os.path.exists(input_csv):
            raise FileNotFoundError(f"Input file '{input_csv}' not found.")

        # Read the input CSV
        df = pd.read_csv(input_csv)
        if df.empty:
            raise ValueError(f"Input file '{input_csv}' is empty.")

        # Ensure required columns are present
        required_columns = ['Ticker', 'First Value', 'Last Value', 'Percentage Change']
        for column in required_columns:
            if column not in df.columns:
                raise KeyError(f"Input CSV must contain the column '{column}'.")

        # Sort the stocks by 'Percentage Change' in descending order
        df = df.sort_values(by='Percentage Change', ascending=False)

        # Select the top 20 tickers
        top_20 = df.head(20)

        # Get the current date for the 'Last update' column
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Calculate 'buy at' and 'stop loss'
        top_20.loc[:, 'buy at'] = top_20['Last Value'] + ((2 / 100) * top_20['Last Value'])
        top_20.loc[:, 'stop loss'] = top_20['Last Value'] * 0.8
        
        # Create a DataFrame for the output format
        output_df = pd.DataFrame({
            'Ticker': top_20['Ticker'],
            'Current Price': top_20['Last Value'].round(3),
            'buy at': top_20['buy at'].round(3),
            'Sell at': (top_20['Last Value'] * 1.2).round(3),  # Sell at 110% of current price
            'stop loss': top_20['stop loss'].round(3),
            'Quantity': 0,  # Set Quantity to 0
            'API Status': 'Buy',  # Set API Status to 'Buy'
            'Balance': 0,  # Placeholder balance
            'Bought at': 0.000,
            'Spare 2': 0,  # Placeholder for Spare 2
            'Last update': current_date,  # Add current date
            'Spare 1': 0.000  # Placeholder for Spare 1
        })

        # Handle duplicates by comparing tickers
        if os.path.exists(output_csv):
            try:
                # Read the existing output file
                existing_df = pd.read_csv(output_csv)

                # Find tickers already present in the output file
                existing_tickers = set(existing_df['Ticker'])

                # Filter out duplicate tickers
                output_df = output_df[~output_df['Ticker'].isin(existing_tickers)]

                # Append only new tickers to the output file
                combined_df = pd.concat([existing_df, output_df], ignore_index=True)
            except Exception as e:
                raise IOError(f"Failed to read or append to the existing output file '{output_csv}': {e}")
        else:
            # If the file doesn't exist, create it with the new data
            combined_df = output_df

        # Write to the output CSV file
        combined_df.to_csv(output_csv, index=False, float_format="%.3f")
        print(f"Appended top 20 stocks to {output_csv}, avoiding duplicates.")

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
    input_csv = 'filtered_stocks.csv'  # Replace with the path to your input file
    output_csv = 'portfolio.csv'  # Replace with the desired output file path
    process_top_20_stocks(input_csv, output_csv)
