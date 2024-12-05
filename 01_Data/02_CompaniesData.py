import pandas as pd
import yfinance as yf
import os

# Function to fetch company data using Yahoo Finance
def fetch_company_data(symbol):
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

        print(f"Data for {symbol} fetched successfully. Company: {company_name}, " +
              f"Sector: {sector}, Industry: {industry}, Market Cap: {market_cap}, " +
              f"P/E Ratio: {p_e_ratio}, P/B Ratio: {p_b_ratio}, PEG Ratio: {peg_ratio}, " +
              f"Dividend Yield: {div_yield}, EPS: {eps}, Revenue: {revenue}, " +
              f"Profit Margin: {profit_margin}, EBITDA: {ebitda}, Earnings Date: {earnings_date}")
        
        return (company_name, sector, industry, market_cap, p_e_ratio, p_b_ratio, 
                peg_ratio, div_yield, eps, revenue, profit_margin, ebitda, earnings_date)
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return ('Not Available', 'Not Available', 'Not Available', 'Not Available', 
                'Not Available', 'Not Available', 'Not Available', 'Not Available', 
                'Not Available', 'Not Available', 'Not Available', 'Not Available', 
                'Not Available')

# Main function to process CSV files
def process_csv(file_path):
    # Define the column names
    columns = [
        'Symbol', 'Company Name', 'Sector', 'Industry', 'Market Capital', 
        'P/E Ratio', 'P/B Ratio', 'PEG Ratio', 'Dividend Yield', 'EPS', 
        'Revenue', 'Profit Margin', 'EBITDA', 'Earnings Date'
    ]
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Creating new file...")
        # Create a new DataFrame with the required structure
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        print(f"New file {file_path} created with the required structure.")
    else:
        # Load the existing file
        df = pd.read_csv(file_path)
        print(f"File {file_path} loaded successfully.")
    
    # Iterate over each row to update company details
    for index, row in df.iterrows():
        symbol = row['Symbol']  # Assuming 'Symbol' is present in the file
        
        # Fetch company data
        company_name, sector, industry, market_cap, p_e_ratio, p_b_ratio, peg_ratio, div_yield, eps, revenue, profit_margin, ebitda, earnings_date = fetch_company_data(symbol)

        # Update the DataFrame with the fetched data
        df.at[index, 'Company Name'] = company_name
        df.at[index, 'Sector'] = sector
        df.at[index, 'Industry'] = industry
        df.at[index, 'Market Capital'] = market_cap
        df.at[index, 'P/E Ratio'] = p_e_ratio
        df.at[index, 'P/B Ratio'] = p_b_ratio
        df.at[index, 'PEG Ratio'] = peg_ratio  
        df.at[index, 'Dividend Yield'] = div_yield
        df.at[index, 'EPS'] = eps
        df.at[index, 'Revenue'] = revenue
        df.at[index, 'Profit Margin'] = profit_margin
        df.at[index, 'EBITDA'] = ebitda
        df.at[index, 'Earnings Date'] = earnings_date  # Add earnings date

    # Save the updated CSV
    df.to_csv(file_path, index=False)
    print(f"CSV file {file_path} updated successfully!")

if __name__ == "__main__":
    # Define file paths
    file = 'Outout_stocks_combined.csv'
    
    # Process the S&P 500 stocks file
    process_csv(file)

