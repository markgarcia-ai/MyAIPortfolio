import csv

def convert_to_csv(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    csv_data = [['Symbol', 'Stock Price', 'Predicted Short Position for Next Month', 'Difference']]

    for line in lines:
        parts = line.strip().split(', ')
        stock = parts[0].split(': ')[1]
        stock_price = float(parts[1].split(': ')[1].replace('$', ''))
        short_position = float(parts[2].split(': ')[1].replace('$', ''))
        difference = round(float(parts[3].split(': ')[1].replace('$', '')), 2)
        csv_data.append([stock, stock_price, short_position, difference])

    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(csv_data)

# Example usage:
"""
input_file = 'predicted_short_positions.txt'  # Replace with your input file name
output_file = 'output.csv'  # Replace with desired output file name
convert_to_csv(input_file, output_file)
"""

if __name__ == '__main__':
    input_file = 'predicted_short_positions_SP500.txt' 
    output_file = 'SP500_output.csv'
    convert_to_csv(input_file, output_file)
    input_file = 'predicted_short_positions_NASDAQ.txt' 
    output_file = 'NASDAQ_output.csv'
    convert_to_csv(input_file, output_file)    
