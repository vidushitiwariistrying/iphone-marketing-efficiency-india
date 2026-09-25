import pandas as pd
import numpy as np
import matplotlib.pyplot as plt # type: ignore
from pytrends.request import TrendReq # type: ignore
import time
#from sqlalchemy import create_engine
pytrend = TrendReq(
    hl='en-IN', 
    tz=-330, 
    retries=3, 
    backoff_factor=2, 
    timeout=(10, 25)
)

launch_17_window= "2025-09-19 2025-09-26"
launch_18_window= '2026-09-18 2026-09-25'

def fetch_india_trends(keywords, timeframe, max_retries=3):
    """
    Fetches data for multiple keywords in a SINGLE payload call to reduce network requests.
    Includes exponential backoff if Google triggers rate limit (HTTP 429).
    """
    for attempt in range(max_retries):
        try:
            # Passing list of keywords reduces total API requests by half
            pytrend.build_payload(keywords, cat=0, timeframe=timeframe, geo='IN', gprop='')
            df = pytrend.interest_over_time()
            
            if not df.empty:
                if 'isPartial' in df.columns:
                    df = df.drop(columns=['isPartial'])
                return df
            
        except Exception as e:
            if "429" in str(e):
                wait_time = (2 ** attempt) * 10 + 5  # Waits 15s, 25s, 45s...
                print(f"Rate limited by Google (429). Waiting {wait_time} seconds before retrying (Attempt {attempt+1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                print(f"Error fetching {keywords}: {e}")
                break
                
    print(f"Failed to retrieve data for {keywords} after retries.")
    return pd.DataFrame()

time.sleep(10)
print("fetching iPhone 17 series search data and PR Buzz data in India...")
df_17=fetch_india_trends("iphone 17", launch_17_window)
pr_17=fetch_india_trends("Apple Event", launch_17_window)
time.sleep(10)
print("fetching iPhone 18 series search data and PR Buzz data in India...")
df_18=fetch_india_trends("iphone 18", launch_18_window)
pr_18=fetch_india_trends("Apple Event", launch_18_window)
time.sleep(10)

if not df_17.empty and not df_18.empty:
    df_17=df_17.reset_index(drop=True)
    df_18=df_18.reset_index(drop=True)
    
    df_17['Launch_Day'] = [f"Day {i}" for i in range(len(df_17))]
    df_18['Launch_Day'] = [f"Day {i}" for i in range(len(df_18))]
    merged_df = pd.merge(
        df_17[['Launch_Day', 'Search_Interest']].rename(columns={'Search_Interest': 'iPhone_17_Series'}),
        df_18[['Launch_Day', 'Search_Interest']].rename(columns={'Search_Interest': 'iPhone_18_Series'}),
        on='Launch_Day',
        how='inner'
    )

avg_17 = merged_df['iPhone_17_Pro_Max'].mean()
avg_18 = merged_df['iPhone_18_Pro_Max'].mean()
pct_change = ((avg_18 - avg_17) / avg_17) * 100

plt.figure(figsize=(10, 5))
plt.plot(merged_df['Launch_Day'], merged_df['iPhone_17_Pro_Max'], label='iPhone 17 Pro Max', marker='o')
plt.plot(merged_df['Launch_Day'], merged_df['iPhone_18_Pro_Max'], label='iPhone 18 Pro Max', marker='s')
plt.title('7-Day Launch Interest: iPhone 17 Pro Max vs iPhone 18 Pro Max')
plt.xlabel('Days Post Launch')
plt.ylabel('Google Trends Relative Interest Index')
plt.legend()
plt.grid(True)
plt.savefig('launch_comparison.png')
plt.show()

