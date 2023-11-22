from portfolio_backtest import Backtest
import pprint
import yfinance as yf
import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

# Portfolio list
# USD
US_tickers=["VOO","QQQ","VGT"]
Gold=["GC=F"]
USD_tickers= US_tickers + Gold

# JPY
JP_tickers=["^N225"]

#Time
Today = pd.to_datetime(datetime.date.today())
Today= Today.strftime('%Y-%m-%d')

#Get deta
df = yf.download(USD_tickers,start="2010-01-01", end=Today, interval = "1d")

# Compute pairwise correlation  
Df_corr = df["Adj Close"].corr().round(3)

# shown graph
fig, ax = plt.subplots(figsize=(12, 9)) 
sns.heatmap(Df_corr,cmap="Reds",vmin=0, vmax=1,annot=True)
plt.savefig('correlation.png')

Data=Backtest(tickers= USD_tickers,start="2010-01-01",end=Today).run()

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
    