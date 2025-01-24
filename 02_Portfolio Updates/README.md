# MyAIPortfolio description
LAST UPDATE : 19th Jan 2025

This is my AI-driven portfolio management system which follows a combine advanced data analytics, machine learning, and optimization to dynamically manage and adapt to changing market conditions. Below is the flowchart:

## TO DO LIST
**1.Basic portfolio:**Create portfolio based on your current investemnts <br>

## Steps to make it run.
It's divided in two big functions <br>
**1.Stock search:** Main script is in 08_Stock_search/main_scrip.py, which is divided in 5 main functions and need to be enabled in the main script<br>
00_Generate_markets : Download basic stock csv information for a specific market.For new markets, a root csv file shall be created with the basic market information such as Symbiol, company names, etc...   <br>
01_Update_markets.py : Updaye existing csv tickers files with latest csv stock data. MANDATORY RUN FOR UPDATES. <br>
02_Stock_changes.py : xxx <br>
03_Generate_portfolio.py : xxx <br>
04_Compute_summary.py : xxx <br>

**2.Trading Bot:** Main script to activate trading bot and allow transaction<br>


## Flow diagram for full integration

<div align="center">
  <h3>Flowchart process</h3>
  <img src="https://github.com/markgarcia-ai/MyAIPortfolio/blob/main/00_Assets/01_Images/AI_Portfolio-Page-3.drawio.png" width="100%" />
</div>

## [1] Get latest stock, ETF and Investment Trusts market data
Get latest data for NYSE, NASDAQ and S&P500. Gathering a diverse range of financial data, including stocks, ETFs, and investment trusts from Yahoo Finance, forms a reliable basis for portfolio construction. This broad data sourcing aids in achieving a balanced risk-return profile, as each asset type behaves differently under various market conditions, providing an inherent layer of diversification.

Scripts : [01_download_data.py]


## [2] Run Neural Network for short positions stimation
Deploying a neural network model to detect short positions is impactful, especially when the model is well-calibrated and fed with meaningful features. Experimenting with multiple architectures or using ensemble methods can refine predictions, enhancing the model's ability to identify high-confidence short positions.

Scripts : [02_Neural_Networks_AllStocks.py] <br>
Output data: predicted_short_position.txt


## [3] Convert data to excel columns 
Data from NN is in text, a script is required to convert data to excel for better analysis. Documenting model predictions in an organized Excel file makes it easy to review and analyze. This record not only improves accessibility for detailed analysis but also offers a chronological view of model performance, helping to track prediction accuracy and refine strategies based on observed trends.

Scripts : [03_ConvertToCSV.py]
Output data: XXXX_output.csv


## [4] Update data to show more company informations. 
Add latest data for the company for each stock for better understanding to select where to invest. Applying technical indicators like momentum, breakout patterns, volume, and trend analyses to identify potential trades creates a data-driven, active trading framework


### 4.1 - Company details 

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

Scripts: [04_1_DetailCompanyData.py]
Output data: 

### 4.2-Sentiment analysis 
Running sentiment analysis on top predicted short positions adds valuable qualitative insight, enabling you to capture shifts in public opinion that numbers alone may overlook. This step sharpens decision-making, helping to anticipate market movements based on public and media sentiment.

Scripts: [4_2_sentiment_analysis.py]
Output data: 


## 5-Stocks selections 
Select stock based on trading with momentum and another strategies learned in the AI traiding course.
Open the output csv data and sort companies with negative short position returns and select three of them. 

Combine NN results with Trading with momentum. Example below:
<div align="center">
  <img src="https://github.com/markgarcia-ai/MyAIPortfolio/blob/main/00_Assets/01_Images/AI_Portfolio-Momentum chart.drawio.png" width="100%" />
</div>


### 5.1-Trading with momentum 
Momentum trading is based on the idea that assets that have been trending in a particular direction (up or down) will continue to do so for some time. It can be applied over longer timeframes, allowing traders to hold positions for days, weeks, or even momnths, depending on the trend. 

<div align="center">
  <img src="https://github.com/markgarcia-ai/MyAIPortfolio/blob/main/00_Assets/01_Images/trading_with_momentum.jpeg" width="100%" />
</div>



Resample adjusted prices, compute log returns, shift returns, generate tradigin Signal, Projected Returns, T-Test and p-value.

Compute log returns ($R_t$) from prices ($P_t$) as your primary momentum indicator:

$$R_t = log_e(P_t) - log_e(P_{t-1})$$ <br>


Scripts: [5_1_TradingWithMomentum.py]
Output data: 


### 5.2-Breakout Strategy 
Breakout trading is centered around specific price levels, such as support and resistance. Traders look for a price to breach these levels to enter a position. While breakouts can be used for various timeframes, they are often associated with sort-term trading, aiming to capture quick profits. 


**Generate Signal:** Compute the highs and Lows in a Window, compute long and short signals, filter signals, Lookahead Close Prices, Lookahead Price returns and compute the signal return.

**Evaluate Signal** : Histogram.

**Outliers**: Kolmogorov-Smirnov Test and Find Outliers.

Scripts: [5_2_BreakoutStrategy.py]
Output data:

### 5.3-Volume analysis 
Volumne is crucial for validating breakouts. A strong breakout accompanied by high volumne suggests that the price momevement is supported by significant trader interest, making it more likely to continue. Often is look to low colume during a breakout as a warning sign that the move may not hold, helping to filter out false signals.
Volume helps assess the strength of a prevailing trend. High volume during price increases indicates strong momentum, while low volume may signal a weakening trend.

Scripts: [5_3_volumne_analysis.py]
Output data: 

## 5.4-Trends graph analysis 
It plots MACD, RSI, Bollinger Bands and Fibonacci Retracement levels for three stocks. 
Run 05_trengs_graph_analysis.py -> Output data: XXXX_stock_plot.png

Scripts: [5_4_trends_graph_analysis.py]
Output data: 

## 5.5-Matrix results [5_5_matrix_results.py]
The matrix selects the best stock out of three based on trends, sentiment results and volume analysis results.
Run 08_matrix_results.py
NOT WORKING 



## 6 - Aplha research and factor modeling  
. <br>

Scripts: [6_Alpha_research_and _factor_modeling.py]
Output data:


## 7 - Smart Beta and Portfolio Optimization 
Smart beta and optimization are essential to fine-tuning portfolio performance, targeting an improved risk-return balance. This process aligns the portfolio’s holdings with specific objectives, such as minimizing volatility or maximizing returns, while simultaneously addressing risks. <br>

Scripts: [7_Smart_Beta_and_Portfolio.py] <br>
Output data: 

Comparaison of the smart beta portfolio to benchmark index and calculate tracking error against the index. <br>
Smart Beta Computes: Index Weights, ETF Weights, Returns, Weighted Returns, Cumulatie Returns and tracking error. <br>
Portfolio Optimization: Compute Covariance, optimal weights using quadratic programming, rebalance portfolio and calculate portfolio turnover <br>



## 8 - Backtesting 
The backtester will perform portfolio optimization that includes transaction costs, and you'll implement it with computational efficiency in mind, to allow for a reasonably fast backtest. Also use performance attribution to identify the major drivers of your portfolio's profit-and-loss (PnL).

Scripts: [08_backtesting.py] <br>
Output data: 

*Invest wisely, and always conduct thorough research or consult with a financial advisor before implementing any investment strategy.*





