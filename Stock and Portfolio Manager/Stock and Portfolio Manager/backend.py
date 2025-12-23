import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import random
import hashlib

# List of stocks for portfolio allocation
STOCKS = {
    'AAPL': {'name': 'Apple Inc', 'sector': 'Technology'},
    'GOOGL': {'name': 'Alphabet Inc', 'sector': 'Technology'},
    'MSFT': {'name': 'Microsoft', 'sector': 'Technology'},
    'AMZN': {'name': 'Amazon', 'sector': 'Consumer'},
    'TSLA': {'name': 'Tesla', 'sector': 'Automotive'},
    'JPM': {'name': 'JP Morgan', 'sector': 'Finance'},
    'JNJ': {'name': 'Johnson & Johnson', 'sector': 'Healthcare'},
    'V': {'name': 'Visa', 'sector': 'Finance'},
    'WMT': {'name': 'Walmart', 'sector': 'Retail'},
    'DIS': {'name': 'Disney', 'sector': 'Media'},
}

def authenticate(username, password):
    """Simple authentication function"""
    return True

def generate_unique_portfolios(token, investment, risk_level, time_goal):
    """Generate 3-5 unique portfolio suggestions based on user parameters"""
    
    # Set seed based on token and parameters for reproducibility
    seed = hash((token, investment, risk_level, time_goal)) % (2**32)
    np.random.seed(seed)
    random.seed(seed)
    
    portfolios = []
    num_portfolios = random.randint(3, 5)
    
    risk_profiles = {
        'high': {'allocation': [0.70, 0.20, 0.10], 'return': 15.5, 'stocks_per': 6},
        'moderate': {'allocation': [0.50, 0.35, 0.15], 'return': 10.2, 'stocks_per': 5},
        'low': {'allocation': [0.30, 0.50, 0.20], 'return': 6.8, 'stocks_per': 4}
    }
    
    profile = risk_profiles.get(risk_level, risk_profiles['moderate'])
    
    for i in range(num_portfolios):
        # Randomly select stocks
        num_stocks = profile['stocks_per']
        selected_stocks = random.sample(list(STOCKS.keys()), min(num_stocks, len(STOCKS)))
        
        # Distribute investment across selected stocks
        allocation = {}
        remaining = investment
        for j, stock in enumerate(selected_stocks[:-1]):
            amount = round(remaining / (len(selected_stocks) - j), 2)
            allocation[stock] = amount
            remaining -= amount
        allocation[selected_stocks[-1]] = round(remaining, 2)
        
        # Calculate returns
        annual_return = profile['return'] + random.uniform(-2, 2)
        if time_goal == 'short':
            months = 6
            monthly_return = annual_return / 12
        else:
            months = 12
            monthly_return = annual_return / 12
        
        future_value = investment * ((1 + monthly_return/100) ** months)
        net_profit = future_value - investment
        
        portfolio = {
            'investment': f"Rs {investment:,.2f}",
            'allocation': allocation,
            'expectedreturn': f"{annual_return:.2f}",
            'returnperiod': 'monthly' if time_goal == 'short' else 'yearly',
            'suggestedduration': f"{'6 months' if time_goal == 'short' else '1 year'}",
            'strategy': f"{risk_level.capitalize()} Risk Portfolio",
            'futurevalue': f"Rs {future_value:,.2f}",
            'netprofit': f"Rs {net_profit:,.2f}"
        }
        
        portfolios.append(portfolio)
    
    return portfolios

def generate_pie_chart(allocation, filename):
    """Generate pie chart for portfolio allocation"""
    try:
        stocks = list(allocation.keys())
        amounts = list(allocation.values())
        
        plt.figure(figsize=(8, 6))
        colors = plt.cm.Set3(np.linspace(0, 1, len(stocks)))
        plt.pie(amounts, labels=stocks, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Portfolio Allocation')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(f'static/{filename}', dpi=100, bbox_inches='tight')
        plt.close()
        return True
    except Exception as e:
        print(f"Error generating pie chart: {e}")
        return False
