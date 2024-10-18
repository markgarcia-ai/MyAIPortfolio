# MyAIPortfolio description

In 01_Files folder we have the different scripts to run the stocks analysis. It doesn't do any portolio checks yet. 
Tasks to check S&P500 and NASDAQ stocks and find short positions <br>

## 1-Get latest stock, ETF and Investment Trusts market data [01_download_data.py]
Get latest data for NYSE, NASDAQ and AMEX. 
Run 01_download_data.py -> Output data: XXXXX_stocks.csv
STATUS : TESTED AND OK 15 Sep 2024

----------------------------------------------------------------------------------------------------------------

## 2-Run Neural Network for short positions stimation. [02_Neural_Networks_AllStocks.py]
Run Neural Network short positions for next month on the next markets: 
NYSE, NASDAQ and AMEX. 
Run 02_Neural_Networks_AllStocks.py -> Outout data: predicted_short_position.txt
STATUS : TESTED AND OK 15 Sep 2024

----------------------------------------------------------------------------------------------------------------

## 3-Convert data to excel columns [03_ConvertToCSV.py]
Data from NN is in text, a script is required to convert data to excel for better analysis.
Run 03_ConvertToCSV.py -> Output data: XXXX_output.csv
STATUS : TESTED AND OK 15 Sep 2024

----------------------------------------------------------------------------------------------------------------

## 4-Update data to show more company informations. [04_CompaniesData.py] 
Add latest data for the company for each stock for better understanding to select where to invest. 
Run 04_CompaniesData.py -> Output data: XXXX_output.csv
STATUS : TESTED AND OK 15 Sep 2024


### 4.1 - Company details [04_1_DetailCompanyData.py]

Below all the company details provided by the AI:

#### 4.1.1 Profabitiliy Ratios: Gross Margin, Net Margin, ROA, ROE<br>
**1. Gross Profit Margin** : Measures the percentage of revenue that exceeds the cost of goods sold (COGS). It indicates how efficiently a company produces and sells its products -> Formula: (Gross Profit / Revenue) * 100 <br>
**2.Operating Profit Margin (EBIT Margin)**: Shows the percentage of revenue left after covering operating expenses, excluding interest and taxes.
Formula: (Operating Income / Revenue) * 100 <br>
**3. Net Profit Margin**: Indicates how much of each dollar earned by the company translates into profit after all expenses, including taxes and interest.
Formula: (Net Income / Revenue) * 100 <br>
**4.Return on Assets (ROA)**: Measures how effectively a company uses its assets to generate profit.
Formula: (Net Income / Total Assets) * 100 <br>
**5.Return on Equity (ROE)**: Shows how well a company uses shareholders' equity to generate profit.
Formula: (Net Income / Shareholders' Equity) * 100 <br>

#### 4.1.2 Liquidity: Current Ratio, Quick Ratio, Cash Ratio <br>
**1.Current Ratio**: Measures the ability of a company to pay its short-term obligations with its short-term assets.
Formula: Current Assets / Current Liabilities <br>
**2.Quick Ratio (Acid-Test Ratio)**: Similar to the current ratio but excludes inventory, giving a stricter view of a company's short-term liquidity.
Formula: (Current Assets - Inventory) / Current Liabilities <br>
**3.Cash Ratio**: The most stringent liquidity measure, showing the ability of a company to cover its short-term liabilities with its cash and cash equivalents.
Formula: Cash and Cash Equivalents / Current Liabilities <br>

#### 4.1.3 Leverage: Debt-to-Equity, Interest Coverage, Debt-to-EBITDA <br>
**1.Debt-to-Equity Ratio**: Indicates how much debt the company uses to finance its assets relative to the value of shareholders' equity.
Formula: Total Debt / Shareholders' Equity <br>
**2.Interest Coverage Ratio**: Measures the company's ability to meet its interest payments on outstanding debt.
Formula: Operating Income / Interest Expense <br>
**3.Debt-to-EBITDA Ratio**: Helps assess the ability of a company to pay off its debt using its earnings before interest, taxes, depreciation, and amortization (EBITDA).
Formula: Total Debt / EBITDA <br>

#### 4.1.4 Efficiency: Asset Turnover, Inventory Turnover <br> 
**1. Asset Turnover Ratio**: Measures how efficiently a company uses its assets to generate revenue.
Formula: Revenue / Total Assets <br>
**2. Inventory Turnover**: Indicates how often a company sells and replaces its inventory over a period.
Formula: Cost of Goods Sold / Average Inventory <br>
**3. Receivables Turnover**: Shows how efficiently a company collects its receivables.
Formula: Net Credit Sales / Average Accounts Receivable <br>

#### 4.1.5 Valuation: P/E, P/B, P/S <br>
**1. Price-to-Earnings (P/E) Ratio**: Compares the price of a stock to its earnings per share (EPS). It indicates how much investors are willing to pay per dollar of earnings. 
Formula: Market Price per Share / Earnings per Share (EPS) <br>
**2.Price-to-Book (P/B) Ratio**: Compares the market price of a stock to its book value.
Formula: Market Price per Share / Book Value per Share <br>
**3. Price-to-Sales (P/S) Ratio**: Measures the value investors place on each dollar of a company’s revenue.
Formula: Market Cap / Total Revenue <br>

#### 4.1.6 Growth: Revenue Growth, Earnings Growth, FCF Growth <br>
**1. Revenue Growth**: Indicates how much a company's revenue is increasing or decreasing over time, reflecting its ability to expand its market share. <br>
**2. Earnings Growth**: Shows the increase in a company’s earnings per share (EPS) over time. <br>
**3. Free Cash Flow (FCF) Growth**: Tracks changes in the company's free cash flow, which is the cash generated after accounting for capital expenditures. <br>
Formula: Cash from Operations - Capital Expenditures <br>

#### 4.1.7 Cash Flow: Operating Cash Flow, Free Cash Flow
**1. Operating Cash Flow**: Measures the cash generated from a company’s core business operations. <br>
**2. Free Cash Flow (FCF)**: Indicates the cash available for distribution among the company's stakeholders. <br>
Formula: Cash from Operations - Capital Expenditures <br>
**3. Cash Flow to Debt Ratio**: Measures a company’s ability to cover its debt using the cash flow from its operations.
Formula: Operating Cash Flow / Total Debt <br>

----------------------------------------------------------------------------------------------------------------

## 5-Stocks selections [Two python scripts]
Open the output csv data and sort companies with negative short position returns and select three of them. 

### 5.1-Trading with momentum [5_1_TradingWithMomentum.py]
Momentum trading is based on the idea that assets that have been trending in a particular direction (up or down) will continue to do so for some time. It can be applied over longer timeframes, allowing traders to hold positions for days, weeks, or even momnths, depending on the trend. 

Resample adjusted prices, compute log returns, shift returns, generate tradigin Signal, Projected Returns, T-Test and p-value.

### 5.2-Breakout Strategy [5_2_BreakoutStrategy.py]
Breakout trading is centered around specific price levels, such as support and resistance. Traders look for a price to breach these levels to enter a position. While breakouts can be used for various timeframes, they are often associated with sort-term trading, aiming to capture quick profits. 


**Generate Signal:** Compute the highs and Lows in a Window, compute long and short signals, filter signals, Lookahead Close Prices, Lookahead Price returns and compute the signal return.

**Evaluate Signal** : Histogram.

**Outliers**: Kolmogorov-Smirnov Test and Find Outliers.


----------------------------------------------------------------------------------------------------------------


## 6-Trends graph analysis [06_trends_graph_analysis.py]
It plots MACD, RSI, Bollinger Bands and Fibonacci Retracement levels for three stocks. 
Run 05_trengs_graph_analysis.py -> Output data: XXXX_stock_plot.png
STATUS : TESTED AND OK 15 Sep 2024

----------------------------------------------------------------------------------------------------------------

## 7-Volume analysis []
Volume is a crucial metric in stock market analysis for several reasons: Liquidity indicator, Market Sentiment, Confirmation of Trends, Preice PAtterns and Technical Analysis, Support and resistance levels, Volatility measurement and avoiding false signals.
Run 06_volume_analysis.py
STATUS : TESTED AND OK 15 Sep 2024

----------------------------------------------------------------------------------------------------------------

## 8-Sentiment analysis []
TBC
Run 07_sentiment_analysis.py
STATUS : TESTED AND OK 15 Sep 2024

----------------------------------------------------------------------------------------------------------------

## 9-Matrix selection []
The matrix selects the best stock out of three based on trends, sentiment results and volume analysis results.
Run 08_matrix_results.py
NOT WORKING 

----------------------------------------------------------------------------------------------------------------

## 10 - Smart Beta and Portfolio Optimization [] -> From AI trading course

Comparaison of the smart beta portfolio to benchmark index and calculate tracking error against the index. <br>
Smart Beta Computes: Index Weights, ETF Weights, Returns, Weighted Returns, Cumulatie Returns and tracking error. <br>
Portfolio Optimization: Compute Covariance, optimal weights using quadratic programming, rebalance portfolio and calculate portfolio turnover <br>

----------------------------------------------------------------------------------------------------------------

## 11 - Portfolio performance comparison []




----------------------------------------------------------------------------------------------------------------

*Invest wisely, and always conduct thorough research or consult with a financial advisor before implementing any investment strategy.*





