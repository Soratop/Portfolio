import yfinance as yf
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.deterministic import DeterministicProcess
from sklearn.linear_model import LinearRegression


#Get deta
def get_df(list,start_time,end_time):
    df=yf.download(list,start=start_time, end=end_time, interval = "1d").reset_index()
    return df


# show graph
def line_graph(Data,x_col_name,y_col_name,title="test",show=True):
    fig,ax=plt.subplots()
    ax.plot(x_col_name,y_col_name,data=Data)
    ax.set_title(title)
    if show:
        plt.show()
        
        
        
        

# Portfolio list
US_tickers=["VOO", "QQQ"] #"VOO","SPXL"
US_Company=["AAPL","MSFT","AMZN","NVDA","GOOGL","GOOG","TSLA","META"]
USD_tickers= US_tickers+US_Company

JP_tickers=["^N225"]
JPY_tickers=JP_tickers

# Exchange rate
JPY=["JPY=X"]
EUR=["EUR=X"]
CNY=["CNY=X"]
BTC=["USD-BTC"]

#other
OIL=["CL=F"]
GOLD=["GC=F"]

# Time
today=pd.to_datetime(datetime.date.today())
tomorrow=pd.to_datetime(datetime.date.today())+datetime.timedelta(days=1)
today=today.strftime('%Y-%m-%d')
start_time="2016-01-01"

# Get deta
df=get_df(USD_tickers,start_time,today)
df_jpy=get_df(JPY,start_time,today)
df_eur=get_df(EUR,start_time,today)

# making moving_average
df_adj=df["Date"]
df_adj=pd.concat([df["Date"],df["Adj Close"]],axis=1)
df_adj= df_adj.set_index("Date").to_period("d")

df_row="VOO"

moving_average = df_adj.rolling(window=365,center=True,min_periods=183).mean()
  
ax = df_adj[df_row].plot(style=".",color="0.5")
moving_average[df_row].plot(
    ax=ax, title= df_row+" "+"365-Day Moving Average", legend=False)

plt.show()

# making DeterministicProcess
dp=DeterministicProcess(
    index=df_adj[df_row].index,
    constant=True,
    order=1,
    drop=True, 
)

X = dp.in_sample()

y = df_adj[df_row]  

model = LinearRegression(fit_intercept=False)
model.fit(X, y)

y_pred = pd.Series(model.predict(X), index=X.index)

ax = df_adj[df_row].plot(style=".", color="0.5", title= df_row+" "+"Linear Trend")
y_pred.plot(ax=ax, linewidth=3, label="Trend")
plt.show()

X = dp.out_of_sample(steps=365)

y_fore = pd.Series(model.predict(X), index=X.index)

print(X)

ax = df_adj["2016":][df_row].plot(title=df_row +" " + "Linear Trend Forecast",color="0.75",
    style=".-",
    markeredgecolor="0.25",
    markerfacecolor="0.25",
    legend=False,)

ax = y_pred["2016":].plot(ax=ax, linewidth=3, label="Trend")
ax = y_fore.plot(ax=ax, linewidth=3, label="Trend Forecast", color="C3")

plt.show()


