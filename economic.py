from fredapi import Fred
from dotenv import load_dotenv
import os

load_dotenv()

def get_economic_data():
    fred = Fred(api_key=os.getenv('FRED_API_KEY'))
    
    # Consumer Sentiment (University of Michigan) — how confident people feel
    sentiment = fred.get_series('UMCSENT', observation_start='2020-01-01')
    
    # Unemployment rate
    unemployment = fred.get_series('UNRATE', observation_start='2020-01-01')
    
    # CPI — inflation
    inflation = fred.get_series('CPIAUCSL', observation_start='2020-01-01')
    
    print("=== ECONOMIC DATA ===")
    print(f"\nConsumer Sentiment (latest): {sentiment.iloc[-1]:.1f}")
    print(f"  (100 = neutral, above = optimistic, below = pessimistic)")
    print(f"\nUnemployment Rate (latest): {unemployment.iloc[-1]:.1f}%")
    print(f"\nCPI Inflation Index (latest): {inflation.iloc[-1]:.1f}")
    
    return {
        "sentiment": sentiment,
        "unemployment": unemployment,
        "inflation": inflation
    }

if __name__ == "__main__":
    get_economic_data()