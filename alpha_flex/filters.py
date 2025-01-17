FILTERS = {
    "High Growth": {
        'Market Cap.': '+Large (over $10bln)',  # Adjusted to valid range
        'EPS growthqtr over qtr': 'Over 40%',
        'EPS growthnext year': 'Over 30%',
        'EPS growththis year': 'Over 30%',
        'Sales growthqtr over qtr': 'Over 30%',
        'Average Volume': 'Over 1M',
        'RSI (14)': 'Not Oversold (>50)',
        '200-Day Simple Moving Average': 'Price above SMA200',
        'Debt/Equity': 'Under 0.5',
        'Gross Margin': 'Over 40%'
    },
    
    "High Sales Growth": {
        'Market Cap.': '+Mid (over $2bln)',  # Corrected to valid option
        'Debt/Equity': 'Under 0.3',
        'Gross Margin': 'Over 60%',
        'Return on Equity': 'Over +25%',
        'Sales growthpast 5 years': 'Over 20%',
        'Sales growthqtr over qtr': 'Over 25%',
        'Average Volume': 'Over 500K',
        'InstitutionalOwnership': 'Over 80%',
        'Price': 'Over $10',
        'Short Float': 'Under 5%'
    },
    
    "Buy and Hold": {
        'Market Cap.': '+Mid (over $2bln)',  # Corrected to valid option
        'Current Ratio': 'Over 2',
        'EPS growthnext 5 years': 'Over 15%',
        'PEG': 'Under 2',
        'Return on Equity': 'Over +15%',
        'Beta': 'Under 1.5',
        '20-Day Simple Moving Average': 'Price above SMA20',
    },

    "Bullish": {
        'Market Cap.': '+Mid (over $2bln)',  # Corrected to valid option
        'EPS growthpast 5 years': 'Positive (>0%)',
        'EPS growthqtr over qtr': 'Over 20%',
        'EPS growththis year': 'Over 25%',
        'EPS growthnext year': 'Over 15%',
        'EPS growthnext 5 years': 'Over 15%',
        'Return on Equity': 'Over +15%',
        'InstitutionalOwnership': 'Over 50%',
        'Price': 'Over $15',
        '52-Week High/Low': '90% or more above Low',
        'RSI (14)': 'Not Oversold (>50)',
        '50-Day Simple Moving Average': 'Price above SMA50'
    }
}
