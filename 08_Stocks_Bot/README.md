
# Functions

**1.Stock search:** Main script is in 08_Stock_search/main_scrip.py, which is divided in 5 main functions and need to be enabled in the main script<br>

## 00_Generate_markets <br> 
Status : Released, pending PR <br>
Download basic stock csv information for a specific market.For new markets, a root csv file shall be created with the basic market information such as Symbiol, company names, etc...   <br>

## 01_Update_markets.py : <br> 
Status : Released, pending PR <br>
Updaye existing csv tickers files with latest csv stock data. MANDATORY RUN FOR UPDATES. <br>
Output files in folders : "Market_DJIA_data", "Market_NASDAQ_data","Market_nyse_data","Market_SP500_data","Market_SP600_data" <br>

## 02_Stock_changes.py : xxx <br>
Status : Released, pending PR <br>
It checks the % change in all stocks, looks for the 20 best and adds company information <br> 
Input files : "dow_jones_stocks.csv","nasdaq_stocks.csv", nyse_tickers.csv","sp500_stocks.csv","sp600_stocks.csv"   <br>
Output file1 : "combined_percentage_changes.csv" -> All stocks <br>
Output file2 : "filtered_stocks.csv" -> Only 20 filtered stocks<br>

## 03_Generate_portfolio.py : xxx <br>
Status : Released, pending PR <br>
It creates a file with the 20 filtered stocks with the portfolio fomrat : Ticker, current price, buy at, sell at, etc... <br>
Explanation. <br>
Input files for all stocks: 'combined_percentage_changes.csv'<br>
Introduce manually tickers in the script for own portfolio'<br>
Output files 1: 'tickers_portfolio.csv'<br>
Output files 2: 'top_n_portfolio.csv'<br>

## 04_Update_portfolio.py : xxx <br>
Status : Script work in progress<br>
It checks the tickers_portfolio.csv file and the current portfolio, updates the new values in the portfolio and makes a copy for the trading bot<br>
Input files : 'tickers_portfolio.csv' <br>
Input files 2: 'current_portfolio.csv' <br>
Output files : <br>

## 05_Compute_summary.py : xxx <br>
I don't remember why I wanted this.... 
Explanation. <br>
Output files : <br>

## Next steps <br>
The stocks trading bot gets the current portfolio, checks the current market and tells you if to sell or buy more.
