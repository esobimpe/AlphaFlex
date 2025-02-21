import os
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime
from .portfolio import get_portfolio  # Assuming get_portfolio() is imported

def backtest_portfolio(initial_investment, period='1y', csv_file='portfolio_data.csv'):
    """
    Perform backtesting for the given portfolio with the specified investment amount and period.
    """
    # Fetch portfolio data from CSV (if recent) or update it
    if os.path.exists(csv_file) and (datetime.now() - datetime.fromtimestamp(os.path.getmtime(csv_file))).days < 1:
        print("Using cached portfolio data.")
        stock_weights = pd.read_csv(csv_file)
    else:
        print("Fetching updated portfolio data...")
        stock_weights = get_portfolio()
        if stock_weights.empty:
            print("Error: Portfolio data is empty. Exiting backtest.")
            return None
        stock_weights.to_csv(csv_file, index=False)  # Cache for reuse

    # Store tickers and weights
    tickers = stock_weights['Stock']
    weights = stock_weights['Stock Allocation Weight (%)'] / 100  # Convert to decimal

    # Fetch stock price data
    stock_prices = {}
    for ticker in tickers:
        try:
            stock_data = yf.Ticker(ticker).history(period=period)
            if 'Close' in stock_data:
                stock_prices[ticker] = stock_data['Close']
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    # Convert price data to DataFrame and clean NaN values
    price_df = pd.DataFrame(stock_prices).dropna(axis=1)

    if price_df.empty:
        print("No valid stock data retrieved. Exiting backtest.")
        return None

    # Adjust weights to only include stocks that have valid price data
    valid_tickers = price_df.columns
    adjusted_weights = weights.reindex(valid_tickers).fillna(0)
    adjusted_weights /= adjusted_weights.sum()  # Re-normalize

    # Compute portfolio performance
    initial_values = adjusted_weights * initial_investment
    price_change_ratios = price_df.iloc[-1] / price_df.iloc[0]
    final_values = initial_values * price_change_ratios
    total_value_after_period = final_values.sum()

    # Compute percentage return
    percentage_return = ((total_value_after_period - initial_investment) / initial_investment) * 100

    # Create final result dataframe
    final_df = pd.DataFrame({
        'Ticker': valid_tickers,
        'Initial Value': initial_values.reindex(valid_tickers).values,
        'Final Value': final_values.values,
        'Percentage Change': (price_change_ratios - 1).values * 100
    })
    final_df.to_csv('final_file.csv', index=False)

    # Prepare final results
    result = {
        'Period': period,
        'Initial Investment': initial_investment,
        'Investment Value After': total_value_after_period,
        'Percentage Return': percentage_return
    }

    return result
