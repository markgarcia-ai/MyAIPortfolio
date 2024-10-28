import pandas as pd
import yfinance as yf

def calculate_alternative_investment(df, fund_ticker):
    """
    Calculate the gain if the investments were made in a specified fund (e.g., S&P 500 or any other).
    
    Args:
        df (pd.DataFrame): DataFrame containing 'Date', 'Invested (£)', and 'Value (£)'.
        fund_ticker (str): Ticker symbol of the fund to simulate the investment.
    
    Returns:
        pd.DataFrame: DataFrame with the alternative fund's performance.
    """
    # Convert the 'Date' column to datetime
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    
    # Download historical data for the chosen fund
    fund_data = yf.download(fund_ticker, start=df["Date"].min(), end=df["Date"].max())
    
    # Reset index to make the 'Date' column accessible for merging
    fund_data = fund_data.reset_index()[["Date", "Adj Close"]]
    
    # Merge the fund data with the investment dates using merge_asof to get the nearest date before or equal to each investment
    df = pd.merge_asof(df.sort_values("Date"), fund_data, on="Date", direction="backward")
    
    # Check if we got valid price data
    if df["Adj Close"].isna().any():
        print("Warning: Some dates do not have corresponding fund prices. Consider adjusting date ranges.")
    
    # Calculate how much of the fund would have been bought with the first investment
    initial_investment = df["Invested (£)"].iloc[0]
    initial_price = df["Adj Close"].iloc[0]
    df["Fund Equivalent Value"] = (initial_investment / initial_price) * df["Adj Close"]
    
    # Calculate the cumulative value of the alternative investment
    df["Cumulative Fund Value"] = df["Fund Equivalent Value"].cumsum()
    
    return df

# Input: Investment data (date, invested amount, value)
data = {
    "Date": ["18/08/2022", "01/01/2023", "31/08/2023", "01/01/2024", "01/04/2024", "01/05/2024", 
             "31/08/2024", "10/09/2024", "17/09/2024", "21/09/2024", "28/09/2024", "11/10/2024"],
    "Invested (£)": [149.11, 1500.00, 7030.00, 7430.00, 14380.00, 19230.00, 15035.00, 15900.00, 
                     16908.00, 16908.00, 16908.00, 17208.00],
    "Value (£)": [149.11, 1497.62, 7435.09, 9167.94, 15890.25, 20141.79, 17073.47, 16731.73, 
                  17435.00, 17637.00, 17811.00, 17961.00]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Choose a fund to simulate (e.g., S&P 500: "^GSPC", or other funds like "VOO", "SPY", etc.)
fund_ticker = "^GSPC"  # S&P 500 index

# Calculate the alternative investment performance
result_df = calculate_alternative_investment(df, fund_ticker)

# Show the result
print(result_df)

# Optional: Save the results to a CSV file
result_df.to_csv("alternative_investment_comparison.csv", index=False)
