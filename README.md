# MyAIPortfolio description

In 01_Files folder we have the different scripts to run the stocks analysis. It doesn't do any portolio checks yet. 
Tasks to check S&P500 and NASDAQ stocks and find short positions <br>

## 1-Get latest stock market data
Get latest data for NYSE, NASDAQ and AMEX. 
Run 01_download_data.py -> Output data: XXXXX_stocks.csv
STATUS : TESTED AND OK 15 Sep 2024

## 2-Run Neural Network for short positions stimation. 
Run Neural Network short positions for next month on the next markets: 
NYSE, NASDAQ and AMEX. 
Run 02_Neural_Networks_AllStocks.py -> Outout data: predicted_short_position.txt
STATUS : TESTED AND OK 15 Sep 2024

## 3-Convert data to excel columns
Data from NN is in text, a script is required to convert data to excel for better analysis.
Run 03_ConvertToCSV.py -> Output data: XXXX_output.csv
STATUS : TESTED AND OK 15 Sep 2024

## 4-Update data to show more company informations.
Add latest data for the company for each stock for better understanding to select where to invest. 
Run 04_CompaniesData.py -> Output data: XXXX_output.csv
STATUS : TESTED AND OK 15 Sep 2024

## 5-Stocks selections [Manual]
Open the output csv data and sort companies with negative short position returns and select three of them. 

## 6-Trends graph analysis
It plots MACD, RSI, Bollinger Bands and Fibonacci Retracement levels for three stocks. 
Run 05_trengs_graph_analysis.py -> Output data: XXXX_stock_plot.png
STATUS : TESTED AND OK 15 Sep 2024

## 7-Volume analysis
Volume is a crucial metric in stock market analysis for several reasons: Liquidity indicator, Market Sentiment, Confirmation of Trends, Preice PAtterns and Technical Analysis, Support and resistance levels, Volatility measurement and avoiding false signals.
Run 06_volume_analysis.py
STATUS : TESTED AND OK 15 Sep 2024

## 8-Sentiment analysis
TBC
Run 07_sentiment_analysis.py
STATUS : TESTED AND OK 15 Sep 2024

## 9-Matrix selection
The matrix selects the best stock out of three based on trends, sentiment results and volume analysis results.
Run 08_matrix_results.py
NOT WORKING 




