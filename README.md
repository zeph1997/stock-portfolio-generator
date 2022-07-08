# stock-portfolio-generator
Quick development of a simple portfolio generator that uses machine learning to predict stock performance. Also includes sentiment analysis for each sector.

# Intro
This system is built using Flask (Python). It is a monolithic application that hosts both the frontend and backend. Frontend uses Vue but we injected it in instead of using .vue files. We also used Jinja for our frontend. Route to index.html is "/".  

# Instructions
* Install chromedriver version based on your google chrome version (https://chromedriver.chromium.org/)
* Install the required libraries (pip install -r requirements.txt)
* run main.py

# ML Models Used
* Seasonal ARIMA - the predictions look quite linear as the predictions go on, this is because we are predicting too many periods ahead. Idealy ARIMA should predict maybe a few days down the road. However our implementation only allows users to choose time horizon in years. So we are predicting minimally 365 periods ahead. The first few predictions are better.
* LSTM - Removed as we were not able to develop it on time. Can be added for future implementations

# Components
* Selenium and BeautifulSoup to scrape internet for news articles and stock metrics, as well as using yahoo finance screener to narrow stocks by sector
* NLP sentiment analysis on news related to the stock and sector to determine if investors are generally bullish or bearish on the stock/sector
* Cross correlation between sectors (using ETF as proxy for sector) and gold
* Portfolio optimisation using sharpe ratio

# Additional Notes
* The system currently only accepts positive values for expected portfolio returns (as it makes sense, nobody would like to lose money in the long run). However, due to the market downturn in 2022, it is hard to find a portfolio that will generate positive returns as we currently train our ML model on 1 year historical data. So almost all stocks are pointing negative over the last 6 months and will not be able to generate a portfolio for you.
* Testing it on 2021 data, it will be able to generate a portfolio (as seen in the screenshots in the presentation)