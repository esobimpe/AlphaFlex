import os
import time
import yfinance as yf
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

            if results is None or not isinstance(results, pd.DataFrame) or 'Ticker' not in results:
                print(f"No valid data returned for category '{category}'")
                continue

            all_tickers.update(results['Ticker'].unique())

        except Exception as e:
            print(f"Error processing category '{category}': {e}")

    return list(all_tickers)


def fetch_stock_data(tickers):
    """Fetches stock data in batches to prevent hitting Yahoo Finance rate limits."""
    stock_data = []
    max_retries = 3
    retry_delay = 5  # seconds

    # Batch fetch to reduce API calls
    chunk_size = 10  
    ticker_chunks = [tickers[i:i + chunk_size] for i in range(0, len(tickers), chunk_size)]

    for chunk in ticker_chunks:
        for attempt in range(max_retries):
            try:
                stocks = yf.Tickers(" ".join(chunk))
                for ticker in chunk:
                    stock = stocks.tickers.get(ticker)
                    if not stock:
                        continue
                    info = stock.info
                    hist = stock.history(period="1y")

                    stock_data.append({
                        'Stock': ticker,
                        'Name': info.get('shortName', 'N/A'),
                        'Country': info.get('country', 'N/A'),
                        'Sector': info.get('sector', 'N/A'),
                        'Market Cap': info.get('marketCap', 0),
                        'Revenue': info.get('totalRevenue', 0),
                        'Volatility': np.std(hist['Close']) if not hist.empty else 0
                    })
                break  # Exit retry loop if successful
            except Exception as e:
                print(f"Error fetching batch {chunk} (attempt {attempt + 1}/{max_retries}): {e}")
                time.sleep(retry_delay)  # Wait before retrying

    return stock_data


def calculate_portfolio():
    """Calculates stock allocation weights based on different factors."""
    stock_tickers = get_distinct_tickers()
    if not stock_tickers:
        print("No tickers retrieved. Aborting portfolio calculation.")
        return pd.DataFrame()

    data = fetch_stock_data(stock_tickers)
    if not data:
        print("No data fetched for any tickers. Aborting portfolio calculation.")
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df = df[df['Country'].isin(['United States', 'Canada'])]

    if df.empty:
        print("No stocks from US/Canada found. Exiting.")
        return pd.DataFrame()

    # Calculate different weighting metrics
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

    final_df = df[['Stock', 'Name', 'Country', 'Sector', 'Market Cap', 'Revenue', 'Volatility', 'Stock Allocation Weight (%)']]
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
