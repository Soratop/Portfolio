from portfolio_backtest import Backtest
import pprint
import yfinance as yf
import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Portfolio list
# USD
US_tickers=["VOO","QQQ","VGT"]
Gold=["GC=F"]
USD_tickers= US_tickers + Gold

# JPY
JP_tickers=["^N225"]

#Time
Today = pd.to_datetime(datetime.date.today())
Start_time="2015-01-01"
Total_days=(Today-pd.to_datetime(Start_time)).days
Today= Today.strftime('%Y-%m-%d')

#Get deta
df = yf.download(USD_tickers,start=Start_time, end=Today, interval = "1d")

# Check for missing values.
print("Count the Nan")
print(df.isnull().sum())

# Interpolation
df=df.interpolate()
print("After interpolating")
print(df.isnull().sum())

# Compute pairwise correlation
Df_adj_close=df["Adj Close"]
Df_corr = df["Adj Close"].corr().round(3)

# shown graph
fig, ax = plt.subplots(figsize=(12, 9)) 
sns.heatmap(Df_corr,cmap="Reds",vmin=0, vmax=1,annot=True)
plt.savefig('correlation.png')

# Day return
Day_return=1+Df_adj_close.pct_change()

# cumulative sum
cum_return=(1+Df_adj_close.pct_change()).cumprod()

cum_return.plot(figsize=(12,8))
plt.savefig('Returns.png')
#plt.show()

Data=Backtest(tickers= USD_tickers,start="2015-01-01",end=Today).run()

# setting Advanced Run(True or False)
Advanced_run = False

# Get data
if Advanced_run==True:
    bt = Backtest(
        tickers={
        "VOO": 0.6,
        "GC=F": 0.25,
        },
        target_return=0.1,
        target_cvar=0.025,
        data_dir="data",
        start="2020-04-10",
        end="2023-04-10",
        )
    pprint.pprint(bt.run(plot=True))
else:
    Data
    