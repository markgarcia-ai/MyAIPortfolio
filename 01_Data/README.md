# DATA

## [1] Get latest stock, ETF and Investment Trusts market data
Get latest data for NYSE, NASDAQ and S&P500. Gathering a diverse range of financial data, including stocks, ETFs, and investment trusts from Yahoo Finance, forms a reliable basis for portfolio construction. This broad data sourcing aids in achieving a balanced risk-return profile, as each asset type behaves differently under various market conditions, providing an inherent layer of diversification.

Scripts : [01_download_data.py]


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

