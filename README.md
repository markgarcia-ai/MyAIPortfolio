# MyAIPortfolio description

Tasks to update portfolio: 

## 1-Get latest stock market data
Get latest data for NYSE, NASDAQ and AMEX. 
Run 01_download_data.py -> Output data: XXXXX_stocks.csv

## 2-Run Neural Network for short positions stimation. 
Run Neural Network short positions for next month on the next markets: <br>
NYSE, NASDAQ and AMEX. 
Run 02_Neural_Networks_AllStocks.py -> Outout data: predicted_short_position.txt

## 3-Convert data to excel columns
Data from NN is in text, a script is required to convert data to excel for better analysis.
Run 03_ConvertToCSV.py -> Output data: XXXX_output.csv

## 4-Update data to show more company informations.
Add latest data for the company for each stock for better understanding to select where to invest. 
Run 04_CompaniesData.py -> Output data: XXXX_output.csv

## 5-Stocks selections [Manual]
Open the output csv data and sort companies with negative short position returns and select three of them. 

## 6-Trends graph analysis
It plots MACD, RSI, Bollinger Bands and Fibonacci Retracement levels for three stocks. 
Run 05_trengs_graph_analysis.py -> Output data: XXXX_stock_plot.png

## 7-Volume analysis
TBC
Run 06_volume_analysis.py

## 8-Sentiment analysis
TBC
Run 07_sentiment_analysis.py

## 9- Final selection





