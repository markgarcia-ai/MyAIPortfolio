import pandas as pd
import yfinance as yf

# Load the CSV file
file_path = 'output.csv'  # Specify your CSV file path
df = pd.read_csv(file_path)

# Function to fetch company data using Yahoo Finance
def fetch_company_data(symbol):
    try:
        # Use yfinance to get ticker data
        ticker = yf.Ticker(symbol)
        
        # Extract the needed data
        company_name = ticker.info.get('longName', 'N/A')
        sector = ticker.info.get('sector', 'N/A')
        market_cap = ticker.info.get('marketCap', 'N/A')
        financial_results = ticker.info.get('financialCurrency', 'N/A')  # Placeholder for results
        next_financial_statement = ticker.info.get('nextEarningsDate', 'N/A')
        
        return company_name, sector, market_cap, financial_results, next_financial_statement
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'

# Iterate over each row to update company details
for index, row in df.iterrows():
    symbol = row['Symbol']  # Assuming 'Symbol' is column A
    
    # Fetch company data
    company_name, sector, market_cap, financial_results, next_financial_statement = fetch_company_data(symbol)
    
    # Update the DataFrame with the fetched data
    df.at[index, 'Company Name'] = company_name
    df.at[index, 'Sector'] = sector
    df.at[index, 'Market Capital'] = market_cap
    df.at[index, 'Financial Results'] = financial_results
    df.at[index, 'Next Financial Statement'] = next_financial_statement

# Save the updated CSV
df.to_csv(file_path, index=False)

print("CSV file updated successfully!")
