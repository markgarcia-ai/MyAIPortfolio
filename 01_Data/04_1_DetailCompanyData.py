# Install required libraries if not already installed
# !pip install yfinance alpha_vantage fmp_python yahooquery

import requests
import yfinance as yf
from alpha_vantage.fundamentaldata import FundamentalData
from fmp_python.fmp import FMP
from yahooquery import Ticker

# Set API keys
ALPHA_VANTAGE_API_KEY = 'KSD9H9ASYWRBPQKA'
FMP_API_KEY = '0X88EO6E548SPwc1mMn31nzynkAU93Y8'


def get_revenue_and_profit_analysis(ticker_symbol, alpha_vantage_api_key, fmp_api_key):
    """
    Retrieves revenue growth and profit margin data using multiple sources, with error handling.
    """
    print("\n=== Revenue & Profit Analysis ===")
    
    # Try Alpha Vantage first for revenue data
    try:
        fd = FundamentalData(alpha_vantage_api_key)
        income_data, _ = fd.get_income_statement_annual(ticker_symbol)
        
        # Calculate revenue growth using the last two years of data
        revenue_growth = (
            (float(income_data['annualReports'][0]['totalRevenue']) -
             float(income_data['annualReports'][1]['totalRevenue'])) /
            float(income_data['annualReports'][1]['totalRevenue'])
        ) * 100
        
        print(f"Revenue Growth (Last Year - Alpha Vantage): {revenue_growth:.2f}%")
        return revenue_growth
    except Exception as e:
        print(f"Alpha Vantage data retrieval failed: {e}")
    
    # Fallback to Financial Modeling Prep for revenue data
    try:
        fmp_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker_symbol}?apikey={fmp_api_key}&limit=2"
        response = requests.get(fmp_url)
        if response.status_code == 200:
            data = response.json()
            if len(data) >= 2:
                revenue_growth = (
                    (float(data[0]['revenue']) - float(data[1]['revenue'])) /
                    float(data[1]['revenue'])
                ) * 100
                print(f"Revenue Growth (Last Year - Financial Modeling Prep): {revenue_growth:.2f}%")
                return revenue_growth
            else:
                print("Insufficient data from Financial Modeling Prep.")
        else:
            print(f"Failed to retrieve data from Financial Modeling Prep: {response.status_code}")
    except Exception as e:
        print(f"Financial Modeling Prep data retrieval failed: {e}")
    
    # Fallback to yfinance as a last resort
    try:
        stock = yf.Ticker(ticker_symbol)
        financials = stock.financials
        if 'Total Revenue' in financials.index:
            latest_revenue = financials.loc['Total Revenue'][0]
            previous_revenue = financials.loc['Total Revenue'][1]
            revenue_growth = ((latest_revenue - previous_revenue) / previous_revenue) * 100
            print(f"Revenue Growth (Last Year - yfinance): {revenue_growth:.2f}%")
            return revenue_growth
        else:
            print("Revenue data not available via yfinance.")
    except Exception as e:
        print(f"yfinance data retrieval failed: {e}")
    
    print("All sources failed to provide revenue growth data.")
    return None

def get_company_summary(ticker_symbol):
    # Get company summary using yfinance
    stock = yf.Ticker(ticker_symbol)
    info = stock.info
    
    print("=== Company Overview ===")
    print(f"Company: {info.get('longName', 'N/A')}")
    print(f"Ticker: {ticker_symbol}")
    print(f"Description: {info.get('longBusinessSummary', 'N/A')}")
    print(f"Industry: {info.get('industry', 'N/A')}")
    print(f"CEO: {info.get('ceo', 'N/A')}")
    
    print("\n=== Financial Health ===")
    print(f"Gross Profit Margin: {info.get('grossMargins', 'N/A') * 100:.2f}%")
    print(f"Debt to Equity Ratio: {info.get('debtToEquity', 'N/A')}")
    print(f"Revenue Growth (YoY): {info.get('revenueGrowth', 'N/A') * 100:.2f}%")
    print(f"Price to Earnings Ratio (P/E): {info.get('trailingPE', 'N/A')}")
    
    # Perform Revenue & Profit Analysis
    get_revenue_and_profit_analysis(ticker_symbol, ALPHA_VANTAGE_API_KEY, FMP_API_KEY)
    
    # Get company profile using Financial Modeling Prep API
    fmp_url = f"https://financialmodelingprep.com/api/v3/profile/{ticker_symbol}?apikey={FMP_API_KEY}"
    response = requests.get(fmp_url)
    if response.status_code == 200:
        profile = response.json()
        if profile:
            profile = profile[0]
            print("\n=== Management ===")
            print(f"CEO: {profile.get('ceo', 'N/A')}")
            print(f"Sector: {profile.get('sector', 'N/A')}")
            print(f"Company Overview: {profile.get('description', 'N/A')}")
            print(f"Market Cap: ${profile.get('mktCap', 'N/A')}")
            print(f"Exchange: {profile.get('exchange', 'N/A')}")
        else:
            print("Company profile data not available.")
    else:
        print("Failed to retrieve data from Financial Modeling Prep.")
    
    # Get competitor analysis using yahooquery
    ticker = Ticker(ticker_symbol)
    try:
        # Get modules to check if 'summaryProfile' contains industry information
        summary_profile = ticker.summary_profile
        industry = summary_profile.get(ticker_symbol, {}).get('industry', 'N/A')
        
        # Find related tickers (e.g., industry competitors)
        related_tickers = ticker.summary_detail.get(ticker_symbol, {}).get('sector', 'N/A')
        print("\n=== Competitor Analysis ===")
        print(f"Industry: {industry}")
        print(f"Related tickers in the sector: {related_tickers}")
        
        for peer in related_tickers[:5]:  # Limit to 5 peers for brevity
            peer_info = Ticker(peer).summary_detail.get(peer, {})
            print(f"\nCompetitor: {peer}")
            print(f"Revenue Growth: {peer_info.get('revenueGrowth', 'N/A')}")
            print(f"Gross Profit Margin: {peer_info.get('grossMargins', 'N/A')}")
    except Exception as e:
        print(f"Failed to retrieve competitor information: {e}")

    print("\n=== Expected Annual Movement ===")
    try:
        forecast = info.get('earningsForecast')
        print(f"Earnings Growth Forecast (Next Year): {forecast['earningsGrowth'] * 100:.2f}%")
    except (KeyError, TypeError):
        print("Earnings forecast data not available.")


# Example usage
get_company_summary("WBA")  # Replace "MSFT" with the desired company's ticker symbol