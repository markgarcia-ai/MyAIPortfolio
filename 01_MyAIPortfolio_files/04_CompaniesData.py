import pandas as pd
import yfinance as yf

# Function to fetch company data using Yahoo Finance
def fetch_company_data(symbol):
    try:
        # Use yfinance to get ticker data
        ticker = yf.Ticker(symbol)
        
        # Extract the needed data
        company_name = ticker.info.get('longName', 'N/A')
        sector = ticker.info.get('sector', 'N/A')
        industry = ticker.info.get('industry', 'N/A')
        market_cap = ticker.info.get('marketCap', 'N/A')
        p_e_ratio = ticker.info.get('trailingPE', 'N/A')
        p_b_ratio = ticker.info.get('priceToBook', 'N/A')
        peg_ratio = ticker.info.get('pegRatio', 'N/A')
        div_yield = ticker.info.get('dividendYield', 'N/A')
        eps = ticker.info.get('trailingEps', 'N/A')
        revenue = ticker.info.get('totalRevenue', 'N/A')
        profit_margin = ticker.info.get('profitMargins', 'N/A')
        ebitda = ticker.info.get('ebitda', 'N/A')

        return company_name, sector, industry, market_cap, p_e_ratio, p_b_ratio, peg_ratio,div_yield,eps,revenue,profit_margin,ebitda
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return 'N/A','N/A', 'N/A', 'N/A', 'N/A', 'N/A','N/A','N/A', 'N/A', 'N/A', 'N/A', 'N/A'

# Main function to process CSV files
def process_csv(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Iterate over each row to update company details
    for index, row in df.iterrows():
        symbol = row['Symbol']  # Assuming 'Symbol' is column A
        
        # Fetch company data
        company_name, sector, industry, market_cap, p_e_ratio, p_b_ratio, peg_ratio,div_yield,eps,revenue,profit_margin,ebitda = fetch_company_data(symbol)
        
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

    # Save the updated CSV
    df.to_csv(file_path, index=False)
    print(f"CSV file {file_path} updated successfully!")

if __name__ == "__main__":
    # Process the first CSV file
    process_csv('SP500_output.csv')

    # Process the second CSV file
    process_csv('NASDAQ_output.csv')
