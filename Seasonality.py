import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import datetime
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

# check nan
def check_nan(Data):
    if sum(df.isnull().sum())!=0:
        print("data include the NaN")
        return print(df.isnull())
    else:
        return print("Total NaN is zero")
    
    
# Seasonal_plot
def seasonal_plot(X, y, period, freq, ax=None):
    palette = sns.color_palette("husl", n_colors=X[period].nunique(),)
    ax = sns.lineplot(
        x=freq,
        y=y,
        data=X,
        hue=period,
        errorbar=('ci', False),
        ax=ax,
        palette=palette,
        legend=False,
    )
    ax.set_title(f"Seasonal Plot ({period}/{freq})")
    for line, name in zip(ax.lines, X[period].unique()):
        y_ = line.get_ydata()[-1]
        ax.annotate(
            name,
            xy=(1, y_),
            xytext=(6, 0),
            color=line.get_color(),
            xycoords=ax.get_yaxis_transform(),
            textcoords="offset points",
            size=14,
            va="center",
        )
    return ax
    
    

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

# make the Adj Close data
df_adj=df["Date"]
df_adj=pd.concat([df["Date"],df["Adj Close"]],axis=1)
df_adj= df_adj.set_index("Date").to_period("d")

# check NaN 
check_nan(df_adj) 

# Annual Average
df_adj["year"] = df_adj.index.year
#print(df_adj.groupby("year").mean())
df_adj["dayofyear"] = df_adj.index.dayofyear
df_adj["month"] = df_adj.index.month
#df_adj=df_adj.groupby("dayofyear").mean()

# show graph

#fig,(ax0,ax1) = plt.subplots(2,2)
#seasonal_plot(df_adj, y=list(df_adj)[0], period="year", freq="month", ax=ax0[0])
#seasonal_plot(df_adj, y=list(df_adj)[1], period="year", freq="month", ax=ax0[1])
#seasonal_plot(df_adj, y=list(df_adj)[2], period="year", freq="month", ax=ax1[0])
#seasonal_plot(df_adj, y=list(df_adj)[3], period="year", freq="month", ax=ax1[1])

fig,ax = plt.subplots()
seasonal_plot(df_adj, y="VOO", period="year", freq="month", ax=ax)


plt.show()

