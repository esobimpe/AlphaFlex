FILTERS = {
    "High Growth": {
        'Market Cap.': '+Mid (over $5B)',  # Larger companies for stability
        'EPS growthqtr over qtr': 'Over 40%',  # Stronger recent EPS growth
        'EPS growthnext year': 'Over 30%',
        'EPS growththis year': 'Over 30%',
        'Sales growthqtr over qtr': 'Over 30%',  # Reinforced sales momentum
        'Average Volume': 'Over 1M',
        'RSI (14)': 'Not Oversold (>50)',  # More stringent RSI for momentum
        '200-Day Simple Moving Average': 'Price above SMA200',
        'Debt/Equity': 'Under 0.5',  # Ensures financial leverage is manageable
        'Gross Margin': 'Over 40%'  # Profitability at a core level
    },
    
    "High Sales Growth": {
        'Market Cap.': '+Mid (over $2B)',  # Stability while allowing growth potential
        'Debt/Equity': 'Under 0.3',  # Tighter financial leverage filter
        'Gross Margin': 'Over 60%',  # High profitability from operations
        'Return on Equity': 'Over +25%',  # Strong returns for shareholders
        'Sales growthpast 5 years': 'Over 20%',
        'Sales growthqtr over qtr': 'Over 25%',  # Consistent revenue expansion
        'Average Volume': 'Over 500K',  # Moderate liquidity requirement
        'InstitutionalOwnership': 'Over 80%',  # Indicates market confidence
        'Price': 'Over $10',  # Avoid penny stocks
        'Short Float': 'Under 5%'  # Avoids heavily shorted stocks
    },
    
    "Buy and Hold": {
        'Market Cap.': '+Mid (over $2B)',  # More stability for long-term holding
        'Current Ratio': 'Over 2',  # Strong liquidity position
        'EPS growthnext 5 years': 'Over 15%',  # Higher long-term growth projections
        'PEG': 'Under 2',  # Better valuation for growth
        'Return on Equity': 'Over +15%',
        'Beta': 'Under 1.5',
        '20-Day Simple Moving Average': 'Price above SMA20',
    },

    "Bullish": {
        'Market Cap.': '+Mid (over $2B)',  # Avoid speculative small caps
        'EPS growthpast 5 years': 'Positive (>0%)',
        'EPS growthqtr over qtr': 'Over 20%',
        'EPS growththis year': 'Over 25%',
        'EPS growthnext year': 'Over 15%',
        'EPS growthnext 5 years': 'Over 15%',  # Ensures future growth
        'Return on Equity': 'Over +15%',
        'InstitutionalOwnership': 'Over 50%',  # Decent institutional backing
        'Price': 'Over $15',
        '52-Week High/Low': '90% or more above Low',
        'RSI (14)': 'Not Oversold (>50)',  # Strong bullish momentum
        '50-Day Simple Moving Average': 'Price above SMA50'  # Confirms recent trend
    }
}
