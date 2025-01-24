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

## [1] Trading with momentum -> Trading signals branch
**1.Methodology:** Momentum trading involves identifying assets that have shown strong price movements and assuming they will continue in the same direction. It’s often quantified through indicators like moving averages, relative strength index (RSI), or MACD. <br>
**2.Best For:** Short- to medium-term strategies where the goal is to capture trends.
**3.Pros:** Can be highly profitable in trending markets, especially when coupled with risk management. <br>
**4.Cons:** Momentum strategies can underperform in choppy or range-bound markets. <br>


## [2] Breakout strategy -> Breakout Signals branch
**1.Methodology:** The breakout strategy focuses on identifying and capitalizing on assets that break through key price levels (support or resistance). Breakouts often indicate the start of a new trend. <br>
**2.Best For:** Short-term trading where volatility is high, as breakouts can lead to significant price movements. <br>
**3.Pros:** Can lead to quick gains if breakouts turn into sustained trends. <br>
**4.Cons:** Breakouts can often be false, leading to losses if the asset reverses back into the range. <br>


## [3] Smart Beta and Portfolio Optimization  -> Factor Betas
**1.Methodology:** Smart Beta involves constructing a portfolio based on specific factors (e.g., low volatility, dividend yield, or quality) rather than traditional market capitalization weighting. Portfolio optimization, often via mean-variance optimization or risk-parity approaches, seeks the best allocation to maximize risk-adjusted returns. <br>
**2.Best For:** Long-term investors focused on risk-adjusted returns and systematic exposure to specific factors. <br>
**3.Pros:** Provides diversified exposure to risk factors with potential for enhanced returns; often suitable for passive or semi-passive portfolios. <br>
**4.Cons:** Requires ongoing rebalancing and may underperform in certain market environments if factor premiums are not rewarded. <br>


## [4] Alpha Research and Factor Modeling -> Pricing for enhanced Alpha
**1.Methodology:** Alpha research seeks to identify unique sources of excess returns, typically through proprietary signals, quantitative models, or fundamental analysis. Factor modeling involves decomposing returns into known factors (e.g., market, size, value, momentum) to isolate true alpha.<br>
**2.Best For:** Quantitative and fundamental investors who aim to generate excess returns through unique insights, often for active management. <br>
**3.Pros:** When done well, it can consistently generate alpha and differentiate performance. <br>
**4.Cons:** Requires substantial research, data, and expertise; may lead to volatile returns if assumptions are incorrect. <br>


## [5] Combining Signals for Enhanced Alpha
**1.Methodology:** This approach involves aggregating multiple signals—momentum, mean reversion, fundamental, sentiment, macro, etc.—to create a composite signal that can potentially offer a more stable and robust alpha source. <br>
**2.Best For:** Multi-strategy investors or quantitative investors aiming for diversified alpha sources. <br>
**3.Pros:** Reduces reliance on any single strategy, potentially smoothing returns and improving robustness across various market conditions. <br>
**4.Cons:** Requires complex modeling and significant data infrastructure to track, test, and validate multiple signals. <br>
