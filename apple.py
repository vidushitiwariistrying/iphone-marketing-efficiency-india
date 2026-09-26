import pandas as pd
import matplotlib.pyplot as plt 

#loading csv files of google trends data

def load_trends_csv(file_path):
    """
    Reads a Google Trends CSV, skips the top metadeta header, and returns a clean DataFrame
    """
    df=pd.read_csv(file_path, skiprows=1)
    df.columns=['Day','Search_Interest']

    df['Search_Interest']=pd.to_numeric(df['Search_Interest'].astype(str).str.replace('<1','0'),errors='coerce').fillna(0)
    return df

print("Now loading CSV Data")
df_17=pd.read_csv(r"C:\Users\Nisha Tiwari\OneDrive\Desktop\pyproj\iphone17.csv")
df_18=pd.read_csv(r"C:\Users\Nisha Tiwari\OneDrive\Desktop\pyproj\iphone18.csv")
pr_17=pd.read_csv(r"C:\Users\Nisha Tiwari\OneDrive\Desktop\pyproj\keynote25.csv")
pr_18=pd.read_csv(r"C:\Users\Nisha Tiwari\OneDrive\Desktop\pyproj\keynote26.csv")

#aligning dates and merging datasets
df_17['Time']=[f"Day {i}" for i in range(len(df_17))]
df_18['Time']=[f"Day {i}" for i in range(len(df_18))]

merged_df=pd.merge(df_17[['Time','iphone 17']].rename(columns={'Search_Interest':"iPhone 17 Series"}),
                    df_18[['Time','iphone 18']].rename(columns={'Search_Interest':"iPhone 18 Series"}),
                    on='Time', how='inner')

#print(merged_df)
merged_df.to_csv("iphone_india_launch.csv",index=False)
print(merged_df)

#calculating summary and efficiency
total_demand17=merged_df['iphone 17'].sum()
total_demand18=merged_df['iphone 18'].sum()

total_pr17=pr_17['apple event'].sum()
total_pr18=pr_18['apple event'].sum()


efficiency_17=total_demand17/total_pr17 if total_pr17>0 else 0
efficiency_18=total_demand18/total_pr18 if total_pr18>0 else 0

efficiency_change=((efficiency_18 - efficiency_17)/efficiency_17)*100 if efficiency_17>0 else 0

print("Summary Results and Marketing Efficiency\n")
print(f"iPhone 17 Series total demand score:{total_demand17} | PR Buzz:{total_pr17} | Efficiency Ratio:{efficiency_17:.2f}")
print(f"iPhone 18 Series total demand score:{total_demand18} | PR Buzz:{total_pr18} | Efficiency Ratio:{efficiency_18:.2f}")
print(f"Change in Efficiency: {efficiency_change:.2f}% \n")

#visualising the data
plt.figure(figsize=(10,5))
plt.plot(merged_df['Time'], merged_df['iphone 17'], label='iPhone 17 Series (India)', marker='o', color='pink')
plt.plot(merged_df['Time'], merged_df['iphone 18'], label='iPhone 18 Series (India)', marker='s', color='purple')
plt.title('India 7-Day Launch Interest: iPhone 17 Series vs iPhone 18 Series')
plt.xlabel('Days Post Launch Window')
plt.ylabel('Google Trends Relative Interest Index (0-100)')
plt.legend()
plt.grid(True)
plt.savefig('india_launch_comparison.png')
plt.show()

plt.figure(figsize=(7, 5))
series_labels = ['iPhone 17 Series', 'iPhone 18 Series']
efficiencies = [efficiency_17, efficiency_18]

plt.bar(series_labels, efficiencies, color=['yellow', 'blue'], width=0.4)
for i, val in enumerate(efficiencies):
    plt.text(i, val + (val * 0.01), f"{val:.2f}", ha='center', fontweight='bold')
    
plt.title('Marketing Conversion Efficiency (Demand per PR Buzz Point)')
plt.ylabel('Efficiency Ratio (Consumer Demand / PR Buzz)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('india_marketing_efficiency.png')
plt.show()
