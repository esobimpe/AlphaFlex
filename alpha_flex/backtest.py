import os
import requests
import numpy as np
import pandas as pd
from datetime import datetime
from .portfolio import get_portfolio  # Assuming get_portfolio() is imported

# API Details
API_KEY = "8QwKLb4XrUf2fPLAd58pCyHHOKuB3hTX"
BASE_URL = "https://financialmodelingprep.com/api/v3"

def fetch_api_data(endpoint):
    """Helper function to fetch data from the API"""
    url = f"{BASE_URL}/{endpoint}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def fetch_historical_prices(ticker, from_date, to_date):
    """Fetch historical closing prices for a stock within a date range"""
    data = fetch_api_data(f"historical-price-full/{ticker}?from={from_date}&to={to_date}")
    if data and "historical" in data:
        return {day["date"]: day["close"] for day in data["historical"]}
    return {}

def backtest_portfolio(initial_investment, period='1y', csv_file='portfolio_data.csv'):
    """
    Perform backtesting for the given portfolio using API-based historical prices.
    """
    # Define date range for historical prices
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - pd.DateOffset(years=1)).strftime('%Y-%m-%d') if period == '1y' else (datetime.today() - pd.DateOffset(months=6)).strftime('%Y-%m-%d')

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
        historical_prices = fetch_historical_prices(ticker, start_date, end_date)
        if historical_prices:
            stock_prices[ticker] = historical_prices

    # Ensure we have valid stock data
    if not stock_prices:
        print("No valid stock data retrieved. Exiting backtest.")
        return None

    # Convert historical prices to DataFrame
    price_df = pd.DataFrame(stock_prices).T  # Transpose for easier handling
    price_df = price_df.dropna(axis=1)  # Remove columns with missing data

    # Ensure there is enough data to proceed
    if price_df.empty or len(price_df.columns) < 2:
        print("Not enough valid historical data for backtesting. Exiting.")
        return None

    # Adjust weights for available stocks
    valid_tickers = price_df.index
    adjusted_weights = weights.reindex(valid_tickers).fillna(0)
    adjusted_weights /= adjusted_weights.sum()  # Re-normalize

    # Get initial and final prices
    initial_prices = price_df.iloc[:, 0]  # First available date
    final_prices = price_df.iloc[:, -1]  # Last available date

    # Compute portfolio performance
    initial_values = adjusted_weights * initial_investment
    price_change_ratios = final_prices / initial_prices
    final_values = initial_values * price_change_ratios
    total_value_after_period = final_values.sum()

    # Compute percentage return
    percentage_return = ((total_value_after_period - initial_investment) / initial_investment) * 100

    # Create final result dataframe
    final_df = pd.DataFrame({
        'Ticker': valid_tickers,
        'Initial Value': initial_values.values,
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
