from pytrends.request import TrendReq
import pandas as pd

def get_hemline_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    
    keywords = ["mini skirt", "midi skirt", "maxi skirt", "mini dress"]
    pytrends.build_payload(keywords, timeframe='today 5-y', geo='US')
    
    df = pytrends.interest_over_time()
    
    if df.empty:
        print("No data returned — try again in a minute (Google rate limits)")
        return None
    
    df = df.drop(columns=['isPartial'], errors='ignore')
    
    # The core signal: mini vs midi ratio
    # High mini = economic optimism, high midi/maxi = caution
    df['hemline_index'] = df['mini skirt'] - df['midi skirt']
    
    print("=== HEMLINE TREND DATA (last 5 years) ===")
    print(df.tail(10))
    print(f"\nLatest mini skirt score: {df['mini skirt'].iloc[-1]}")
    print(f"Latest midi skirt score: {df['midi skirt'].iloc[-1]}")
    print(f"Hemline Index (mini - midi): {df['hemline_index'].iloc[-1]}")
    print("Positive = people trending toward mini (optimism signal)")
    print("Negative = people trending toward midi/maxi (caution signal)")
    
    return df

if __name__ == "__main__":
    get_hemline_trends()