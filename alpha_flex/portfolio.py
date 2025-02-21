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

def get_distinct_tickers():
    """Fetches unique stock tickers based on predefined filters."""
    foverview = Overview()
    all_tickers = set()
    alpha_safe_tickers = set()
    
    for category, filters in FILTERS.items():
        try:
            print(f"Applying filters for category '{category}': {filters}")
            foverview.set_filter(filters_dict=filters)
            results = foverview.screener_view()

            if results is None or not isinstance(results, pd.DataFrame) or 'Ticker' not in results:
                print(f"No valid data returned for category '{category}'")
                continue

            tickers = set(results['Ticker'].unique())

            # Special handling for ALPHA_SAFE
            if category == "ALPHA_SAFE":
                valid_tickers = set()
                for ticker in tickers:
                    sector_data = fetch_api_data(f"profile/{ticker}?")
                    if sector_data:
                        sector = sector_data[0].get("sector", "")
                        if sector in ["Consumer Cyclical", "Consumer Defensive", "Healthcare"]:
                            valid_tickers.add(ticker)
                
                alpha_safe_tickers.update(valid_tickers)
            else:
                all_tickers.update(tickers)

        except Exception as e:
            print(f"Error processing category '{category}': {e}")

    return list(alpha_safe_tickers), list(all_tickers)


def calculate_portfolio():
    alpha_safe_tickers, other_tickers = get_distinct_tickers()
    print( alpha_safe_tickers)
    if not alpha_safe_tickers and not other_tickers:
        print("No tickers retrieved. Aborting portfolio calculation.")
        return pd.DataFrame()

    data = []
    all_tickers = alpha_safe_tickers + other_tickers
    
    for ticker in all_tickers:
        try:
            quote_data = fetch_api_data(f"quote-short/{ticker}?")
            if not quote_data:
                continue
            price = quote_data[0].get("price", 0)
            volume = quote_data[0].get("volume", 0)

            market_cap_data = fetch_api_data(f"market-capitalization/{ticker}?")
            market_cap = market_cap_data[0].get("marketCap", 0) if market_cap_data else 0

            revenue_data = fetch_api_data(f"income-statement/{ticker}?period=quarter")
            revenue = revenue_data[0].get("revenue", 0) if revenue_data else 0

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
                'Volatility': volatility,
                'Category': 'ALPHA_SAFE' if ticker in alpha_safe_tickers else 'OTHER'
            })
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    df = pd.DataFrame(data)
    if df.empty:
        print("No data fetched for any tickers. Aborting portfolio calculation.")
        return pd.DataFrame()

    # Normalize Weights
    df['Market Cap Weight'] = df['Market Cap'] / df['Market Cap'].sum()
    num_stocks = len(df)
    df['Equal Weight'] = 1 / num_stocks
    df['Fundamental Weight'] = df['Revenue'] / df['Revenue'].sum()
    df['Inverse Volatility'] = 1 / df['Volatility'].replace(0, np.nan)
    df['Volatility Weight'] = df['Inverse Volatility'] / df['Inverse Volatility'].sum()
    df['Log Market Cap'] = np.log(df['Market Cap'] + 1)
    df['Log Market Cap Weight'] = df['Log Market Cap'] / df['Log Market Cap'].sum()

    # Splitting Allocation
    alpha_safe_df = df[df['Category'] == 'ALPHA_SAFE']
    other_df = df[df['Category'] == 'OTHER']

    if not alpha_safe_df.empty:
        alpha_safe_df['Final Weight'] = (alpha_safe_df['Log Market Cap Weight'] / alpha_safe_df['Log Market Cap Weight'].sum()) * 20
    if not other_df.empty:
        other_df['Final Weight'] = (other_df['Log Market Cap Weight'] / other_df['Log Market Cap Weight'].sum()) * 80

    df = pd.concat([alpha_safe_df, other_df])
    df['Stock Allocation Weight (%)'] = df['Final Weight']

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
