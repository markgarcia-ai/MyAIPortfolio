import pandas as pd

def calculate_stock_scores(df):
    """
    Calculate scores for each stock based on multiple financial metrics.
    """
    # Initialize the Score column
    df['Score'] = 0

    # Give higher score to companies with higher Market Capital, Dividend Yield, EPS, Revenue, Profit Margin, EBITDA
    for col in ['Market Capital', 'Dividend Yield', 'EPS', 'Revenue', 'Profit Margin', 'EBITDA']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric
            df['Score'] += df[col].rank(ascending=False)  # Higher values rank better

    # Give lower score to companies with lower P/E Ratio, P/B Ratio, PEG Ratio
    for col in ['P/E Ratio', 'P/B Ratio', 'PEG Ratio']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric
            df['Score'] += df[col].rank(ascending=True)  # Lower values rank better

    return df

def select_top_stocks(file_path, top_n=5):
    """
    Select the top N stocks to invest in based on the calculated scores.
    """
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Ensure the necessary columns exist
    required_columns = [
        'Company Name', 'Sector', 'Industry', 'Market Capital', 
        'P/E Ratio', 'P/B Ratio', 'PEG Ratio', 'Dividend Yield', 
        'EPS', 'Revenue', 'Profit Margin', 'EBITDA', 'Earnings Date'
    ]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Calculate scores for each stock
    df = calculate_stock_scores(df)

    # Sort the DataFrame by the Score column in descending order
    df = df.sort_values(by='Score', ascending=False)

    # Select the top N stocks
    top_stocks = df.head(top_n)

    # Save the results to a new CSV file
    output_file = "top_stocks.csv"
    top_stocks.to_csv(output_file, index=False)
    print(f"The top {top_n} stocks have been saved to {output_file}.")

    return top_stocks

def create_portfolio():
    """
    
    """

    pass

def function5():
    print("Function 5 from 05_Stock_selection.py")
    # Path to the CSV file
    file_path = "Output_stocks_combined.csv"  # Replace with the path to your CSV file

    # Select the top 5 stocks
    top_stocks = select_top_stocks(file_path, top_n=5)

    # Print the results
    print("Top 5 Stocks to Invest In:")
    print(top_stocks[['Company Name', 'Sector', 'Industry', 'Score']])
    print("Function 5 completed.")