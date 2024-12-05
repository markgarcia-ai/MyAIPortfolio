import csv

# List of input files
input_files = [
    "predicted_short_positions_NASDAQ.txt",  # Replace with your file paths
    "predicted_short_positions_SP500.txt"
]
output_file = "Outout_stocks_combined.csv"  # Name of the resulting CSV file

# Function to parse text files and merge into a CSV
def parse_text_to_csv(input_files, output_file):
    try:
        # Define the CSV header
        header = ["Symbol", "Current Stock Price", "Predicted Short Position", "Difference"]
        rows = []

        # Process each input file
        for input_file in input_files:
            with open(input_file, 'r') as txt_file:
                lines = txt_file.readlines()

            # Process each line and extract relevant data
            for line in lines:
                parts = line.split(", ")
                symbol = parts[0].split(": ")[1]
                current_price = parts[1].split(": ")[1]
                predicted_price = parts[2].split(": ")[1]
                difference = parts[3].split(": ")[1]

                # Add to rows list
                rows.append([symbol, current_price, predicted_price, difference])

        # Write all data to the output CSV
        with open(output_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)  # Write the header
            writer.writerows(rows)  # Write all rows

        print(f"CSV file '{output_file}' has been created successfully with data from {len(input_files)} files.")

    except FileNotFoundError as e:
        print(f"Error: One or more files not found. Details: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
parse_text_to_csv(input_files, output_file)
