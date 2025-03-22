import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import requests
from .config import get_api_key, BASE_URL

def fetch_historical_data(ticker, start_date, end_date):
    """
    Fetch historical adjusted close data for a specific ticker between start_date and end_date.
    """
    api_key = get_api_key()
    url = f"{BASE_URL}/historical-price-full/{ticker}?from={start_date}&to={end_date}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Extract the adjusted close prices
        historical_data = [
            {'date': entry['date'], 'adjClose': entry['adjClose']}
            for entry in data['historical']
        ]
        return pd.DataFrame(historical_data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def backtest_portfolio(initial_investment, period='1y', csv_file='portfolio_data.csv'):
    """
    Perform backtest for the given portfolio with the specified investment amount and period.
    """
    # Check if the CSV file exists and if it's older than 24 hours
    if os.path.exists(csv_file) and (datetime.now() - datetime.fromtimestamp(os.path.getmtime(csv_file))).days < 1:
        print("Fetching Portfolio data.")
        stock_weights = pd.read_csv(csv_file)
    else:
        print("Fetching updated portfolio data...")
        stock_weights = get_portfolio()  # Assuming this fetches the portfolio stock data
        stock_weights.to_csv(csv_file, index=False)  # Cache to CSV

    # Prepare the periods and initialize value_data dictionary
    value_data = {'Ticker': stock_weights['Stock'], 'Weights': stock_weights['Stock Allocation Weight (%)']}

    # Loop through the periods and fetch stock data
    stock_prices = {}
    for stock in stock_weights['Stock']:
        try:
            # Calculate start and end date for the given period
            end_date = datetime.now().strftime('%Y-%m-%d')
            if period == '1m':
                start_date = (datetime.now() - pd.Timedelta(days=30)).strftime('%Y-%m-%d')
            elif period == '3m':
                start_date = (datetime.now() - pd.Timedelta(days=90)).strftime('%Y-%m-%d')
            elif period == '5d':
                start_date = (datetime.now() - pd.Timedelta(days=5)).strftime('%Y-%m-%d')
            elif period == '6m':
                start_date = (datetime.now() - pd.Timedelta(days=182)).strftime('%Y-%m-%d')
            elif period == '1y':
                start_date = (datetime.now() - pd.Timedelta(days=365)).strftime('%Y-%m-%d')
            elif period == '2y':
                start_date = (datetime.now() - pd.Timedelta(days=730)).strftime('%Y-%m-%d')
            elif period == '3y':
                start_date = (datetime.now() - pd.Timedelta(days=1095)).strftime('%Y-%m-%d')
            elif period == 'ytd':  # YTD calculation
                start_date = f'{datetime.now().year}-01-01'
            elif period == '1d':  # 1 Day calculation (yesterday to today)
                # For 1-day period, get data from yesterday to today
                yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                start_date = yesterday
            else:
                raise ValueError(f"Unsupported period: {period}")

            # Fetch historical adjusted close prices using the new API function
            stock_data = fetch_historical_data(stock, start_date, end_date)
            
            if not stock_data.empty:
                # Ensure the dates are sorted, so we can calculate the change correctly
                stock_data = stock_data.sort_values(by='date')
                stock_prices[stock] = stock_data.set_index('date')['adjClose']
            else:
                stock_prices[stock] = None
        except Exception as e:
            stock_prices[stock] = None

    # Convert stock prices to DataFrame
    price_df = pd.DataFrame(stock_prices)

    if price_df.empty:
        value_data[f'{period} Value'] = [np.nan] * len(stock_weights)
    else:
        # Normalize the weights
        stock_weights['Normalized Weight'] = stock_weights['Stock Allocation Weight (%)'] / stock_weights['Stock Allocation Weight (%)'].sum()
        weights = stock_weights.set_index('Stock')['Normalized Weight']
        weights = weights.reindex(price_df.columns).fillna(0)

        # Calculate initial stock values and price change ratios
        initial_stock_values = weights * initial_investment
        # Calculate the price change ratios using adjusted close prices
        price_change_ratios = price_df.iloc[-1] / price_df.iloc[0]  # Last / First
        final_stock_values = initial_stock_values * price_change_ratios
        value_data[f'{period} Value'] = final_stock_values.reindex(stock_weights['Stock']).fillna(0).values

    value_data['Initial Value'] = (stock_weights['Stock Allocation Weight (%)'] / 100) * initial_investment
    final_df = pd.DataFrame(value_data)

    # Save the result to CSV for future use
    final_df.to_csv('final_file.csv', index=False)

    # Get the portfolio values for the specified period
    value_after_period = final_df[f'{period} Value'].sum()

    # Calculate percentage return
    percentage_return = (value_after_period - initial_investment) / initial_investment * 100

    # Prepare the result dictionary
    result = {
        'Period': period,
        'Initial Investment': initial_investment,
        'Investment Value After': value_after_period,
        'Percentage Return': percentage_return
    }

    return result
