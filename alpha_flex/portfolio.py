import os
import time
import yfinance as yf
import requests
import numpy as np
import pandas as pd
from finvizfinance.screener.overview import Overview
from .filters import FILTERS

CSV_FILE_PATH = "./portfolio_data.csv"
EXPIRATION_TIME = 86400  # 24 hours in seconds


def get_distinct_tickers():
    """Fetches unique stock tickers based on predefined filters."""
    foverview = Overview()

    all_tickers = set()
  
    for category, filters in FILTERS.items():
        try:
            print(f"Applying filters for category '{category}': {filters}")
            foverview.set_filter(filters_dict=filters)
            results = foverview.screener_view()

            print(results)

            if results is None or not isinstance(results, pd.DataFrame) or 'Ticker' not in results:
                print(f"No valid data returned for category '{category}'")
                continue

            # Filter based on the 'USA' column if it exists
            if 'USA' in results.columns:
                results_usa = results[results['USA'] == True]  # Assuming True indicates USA
                all_tickers.update(results_usa['Ticker'].unique())
            else:
                print(f"No 'USA' column found in the results for category '{category}'")
                all_tickers.update(results['Ticker'].unique())

        except Exception as e:
            print(f"Error processing category '{category}': {e}")

    return list(all_tickers)


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

def calculate_portfolio():
    stock_tickers = get_distinct_tickers()
    if not stock_tickers:
        print("No tickers retrieved. Aborting portfolio calculation.")
        return pd.DataFrame()
    
    data = []
    for ticker in stock_tickers:
        try:
            # Fetch stock price and volume
            quote_data = fetch_api_data(f"quote-short/{ticker}?")
            if not quote_data:
                continue
            price = quote_data[0].get("price", 0)
            volume = quote_data[0].get("volume", 0)
            
            # Fetch market cap
            market_cap_data = fetch_api_data(f"market-capitalization/{ticker}?")
            market_cap = market_cap_data[0].get("marketCap", 0) if market_cap_data else 0
            
            # Fetch revenue
            revenue_data = fetch_api_data(f"income-statement/{ticker}?period=quarter")
            revenue = revenue_data[0].get("revenue", 0) if revenue_data else 0
            
            # Fetch historical price data for volatility
            hist_data = fetch_api_data(f"historical-price-full/{ticker}?from=2024-01-01&to=2025-01-01")
            if hist_data and "historical" in hist_data:
                closes = [day["close"] for day in hist_data["historical"]]
                volatility = np.std(closes) if closes else 0
            else:
                volatility = 0
            
            data.append({
                'Stock': ticker,
                'Market Cap': market_cap,
                'Revenue': revenue,
                'Volatility': volatility
            })
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    
    df = pd.DataFrame(data)
    if df.empty:
        print("No data fetched for any tickers. Aborting portfolio calculation.")
        return pd.DataFrame()
    
    total_market_cap = df['Market Cap'].sum()
    df['Market Cap Weight'] = df['Market Cap'] / total_market_cap
    num_stocks = len(stock_tickers)
    df['Equal Weight'] = 1 / num_stocks
    total_revenue = df['Revenue'].sum()
    df['Fundamental Weight'] = df['Revenue'] / total_revenue
    df['Inverse Volatility'] = 1 / df['Volatility'].replace(0, np.nan)
    total_inverse_vol = df['Inverse Volatility'].sum()
    df['Volatility Weight'] = df['Inverse Volatility'] / total_inverse_vol
    df['Log Market Cap'] = np.log(df['Market Cap'] + 1)
    df['Log Market Cap Weight'] = df['Log Market Cap'] / df['Log Market Cap'].sum()
    total_capped_weight = df['Log Market Cap Weight'].sum()
    df['Final Capped Weight'] = (df['Log Market Cap Weight'] / total_capped_weight) * 100

    df['Adjusted Weight'] = (
        df['Final Capped Weight'] * 0.3 +
        df['Equal Weight'] * 0.15 +
        df['Volatility Weight'] * 0.15 +
        df['Fundamental Weight'] * 0.4
    )

    total_adjusted_weight = df['Adjusted Weight'].sum()
    df['Stock Allocation Weight (%)'] = (df['Adjusted Weight'] / total_adjusted_weight) * 100

    final_df = df[['Stock', 'Market Cap', 'Revenue', 'Volatility', 'Stock Allocation Weight (%)']]
    return final_df.sort_values(by='Stock Allocation Weight (%)', ascending=False)

def get_portfolio():
    """Fetches portfolio data, either from cache or by recalculating it."""
    if os.path.exists(CSV_FILE_PATH):
        file_mod_time = os.path.getmtime(CSV_FILE_PATH)
        current_time = time.time()

        if current_time - file_mod_time < EXPIRATION_TIME:
            print("Loading portfolio data from cache.")
            return pd.read_csv(CSV_FILE_PATH)

        print("Portfolio data is older than 24 hours. Fetching new data.")
    
    # Fetch new data and save it
    print("Fetching data and creating a cache for the next 24 hours.")
    portfolio_data = calculate_portfolio()
    if not portfolio_data.empty:
        portfolio_data.to_csv(CSV_FILE_PATH, index=False)
    return portfolio_data
