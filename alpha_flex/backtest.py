# your_library/backtest.py

import os
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime
from .portfolio import get_portfolio  # Import get_portfolio() to fetch portfolio data

def backtest_portfolio(investment_amount, period='1y', risk_free_rate=4.52, csv_file='./portfolio_data.csv'):
    """
    Perform backtest for the given portfolio with the specified investment amount and period.
    """
    # Check if the CSV file exists and if it's older than 24 hours
    if os.path.exists(csv_file) and (datetime.now() - datetime.fromtimestamp(os.path.getmtime(csv_file))).days < 1:
        print("Fetching portfolio data from database...")
        stock_weights = pd.read_csv(csv_file)
    else:
        print("Fetching new portfolio data...")
        stock_weights = get_portfolio()  # Assuming this fetches the portfolio stock data
        stock_weights.to_csv(csv_file, index=False)  # Cache to CSV

    # Extract the portfolio stock tickers and weights
    tickers = stock_weights['Stock']
    weights = stock_weights['Stock Allocation Weight (%)'] / 100  # Convert percentage to decimal for weights

    # Fetch stock price data for the selected period
    stock_prices = {}
    for ticker in tickers:
        try:
            stock_data = yf.Ticker(ticker).history(period=period)['Close']
            stock_prices[ticker] = stock_data
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            stock_prices[ticker] = None
    
    # Create a dataframe with the stock prices
    price_df = pd.DataFrame(stock_prices).dropna(axis=1)
    if price_df.empty:
        raise ValueError("No valid stock price data available for the given period.")

    # Calculate portfolio value changes
    price_change_ratios = price_df.iloc[-1] / price_df.iloc[0]
    initial_stock_values = weights * investment_amount
    final_stock_values = initial_stock_values * price_change_ratios
    portfolio_value_after = final_stock_values.sum()

    # Calculate percentage return
    percentage_return = (portfolio_value_after - investment_amount) / investment_amount * 100

    # Calculate volatility (standard deviation of returns)
    daily_returns = price_df.pct_change().dropna()
    portfolio_daily_returns = (daily_returns * weights).sum(axis=1)
    
    # Annualize volatility based on the number of trading days in a year (252 days)
    annualized_volatility = portfolio_daily_returns.std() * np.sqrt(252)  # Annualized volatility
    
    # Adjust volatility if a different period is specified
    if period != '1y':
        # Calculate the number of trading days for the given period
        period_days = {
            '1d': 1,
            '5d': 5,
            '1mo': 21,   # Roughly 21 trading days in a month
            '3mo': 63,   # Roughly 63 trading days in 3 months
            '6mo': 126,  # Roughly 126 trading days in 6 months
            '1y': 252,   # 252 trading days in a year
            '2y': 504,   # 504 trading days in 2 years
            '5y': 1260   # 1260 trading days in 5 years
        }
        
        annualized_volatility = portfolio_daily_returns.std() * np.sqrt(252 / period_days.get(period, 252))

    # Calculate Sharpe ratio (assuming a risk-free rate provided in percentage)
    # Convert the risk-free rate from percentage to decimal
    risk_free_rate = risk_free_rate / 100  # If the user provides a percentage (e.g., 5), divide by 100
    
    sharpe_ratio = (portfolio_daily_returns.mean() - risk_free_rate) / annualized_volatility

    # Prepare the result dictionary
    result = {
        'Period': period,
        'Investment Amount': investment_amount,
        'Investment Value After': portfolio_value_after,
        'Percentage Return': percentage_return,
        'Volatility': annualized_volatility,
        'Sharpe Ratio': sharpe_ratio
    }

    return result
