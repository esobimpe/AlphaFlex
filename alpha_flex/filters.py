FILTERS = {
    "High Growth": {
        'Market Cap.': '+Large (over $10bln)',  # Focus on larger, more stable companies with growth potential.
        'EPS growthqtr over qtr': 'High (>25%)',  # Ensures strong quarterly earnings momentum.
        'EPS growthnext year': 'Over 30%',  # Targets companies expected to sustain high earnings growth in the near future.
        'EPS growththis year': 'Over 30%',  # Filters for companies with exceptional current year growth.
        'Sales growthqtr over qtr': 'Over 30%',  # Looks for businesses with high recent revenue growth.
        'Average Volume': 'Over 1M',  # Ensures sufficient liquidity for ease of trading.
        'RSI (14)': 'Not Oversold (>50)',  # Focuses on stocks with bullish momentum and avoids oversold positions.
        '200-Day Simple Moving Average': 'Price above SMA200',  # Confirms that the stock is in a long-term upward trend.
        'Debt/Equity': 'Under 0.5',  # Limits companies with excessive leverage, ensuring financial health.
        'Gross Margin': 'Over 40%'  # Indicates good profitability at a core business level.
    },
    
    "High Sales Growth": {
        'Market Cap.': '+Mid (over $2bln)',  # Includes medium to larger companies for growth with stability.
        'Debt/Equity': 'Under 0.3',  # Further tightens leverage criteria for stronger financials.
        'Gross Margin': 'Over 60%',  # Focuses on highly profitable companies in terms of operational efficiency.
        'Return on Equity': 'Over +25%',  # Targets companies generating excellent returns for shareholders.
        'Sales growthpast 5 years': 'Over 20%',  # Ensures consistent revenue growth over a longer time frame.
        'Sales growthqtr over qtr': 'Over 25%',  # Looks for businesses with strong recent revenue growth.
        'Average Volume': 'Over 500K',  # Ensures sufficient liquidity while allowing for smaller companies.
        'InstitutionalOwnership': 'Over 80%',  # Highlights confidence from large, professional investors.
        'Price': 'Over $10',  # Avoids penny stocks, ensuring a certain level of market maturity.
        'Float Short': 'Under 5%'  # Avoids heavily shorted stocks, reducing downside risk.
    },
    
    "Buy and Hold": {
        'Market Cap.': '+Mid (over $2bln)',  # Prioritizes medium and large-cap companies for long-term stability.
        'Current Ratio': 'Over 2',  # Indicates strong liquidity and the ability to meet short-term obligations.
        'EPS growthnext 5 years': 'Over 15%',  # Focuses on companies with high projected long-term earnings growth.
        'PEG': 'Under 2',  # Screens for growth stocks that are reasonably valued relative to their growth potential.
        'Return on Equity': 'Over +15%',  # Highlights companies with strong shareholder returns.
        'Beta': 'Under 1.5',  # Targets stocks with lower volatility relative to the market.
        '20-Day Simple Moving Average': 'Price above SMA20',  # Confirms a short-term bullish trend.
    },

    "Bullish": {
        'Market Cap.': '+Mid (over $2bln)',  # Avoids small speculative companies for a more balanced risk.
        'EPS growthpast 5 years': 'Positive (>0%)',  # Focuses on companies with positive long-term earnings growth.
        'EPS growthqtr over qtr': 'Over 20%',  # Indicates strong recent earnings momentum.
        'EPS growththis year': 'Over 25%',  # Focuses on high-growth companies in the current year.
        'EPS growthnext year': 'Over 15%',  # Looks for sustained earnings growth into the next year.
        'EPS growthnext 5 years': 'Over 15%',  # Ensures solid long-term growth expectations.
        'Return on Equity': 'Over +15%',  # Targets companies with strong returns for investors.
        'InstitutionalOwnership': 'Over 50%',  # Indicates confidence from institutional investors.
        'Price': 'Over $15',  # Avoids low-priced stocks, ensuring market quality.
        '52-Week High/Low': '90% or more above Low',  # Focuses on stocks near their 52-week high, indicating strong performance.
        'RSI (14)': 'Not Oversold (>50)',  # Avoids oversold stocks and targets those in bullish momentum.
        '50-Day Simple Moving Average': 'Price above SMA50'  # Confirms recent upward price trends.
    }
}
