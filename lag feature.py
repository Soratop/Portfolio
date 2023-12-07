import yfinance as yf
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

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
 
# making coor     
def corr(data):
    data=data["Adj Close"].corr().round(3)
    return data

# show heatmap
def heatmap(df_corr,show=True):
    fig, ax = plt.subplots(figsize=(12, 9)) 
    sns.heatmap(df_corr,cmap="Reds",vmin=0, vmax=1,annot=True)
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
start_time="2010-01-01"

# Get deta
df=get_df(USD_tickers,start_time,today)
df_jpy=get_df(JPY,start_time,today)
df_eur=get_df(EUR,start_time,today)

# making graph        
line_graph(df,"Date","Adj Close",USD_tickers,show=True)

# making test
test=pd.DataFrame(pd.date_range(start=tomorrow,end=tomorrow+datetime.timedelta(days=364),freq='d'),columns=["Date"])
test["Adj Close"]=0

# making corr 
df_corr=get_df(USD_tickers,start_time,today)
heatmap(corr(df_corr))

# delay 30 day
df_adj=df['Adj Close']
for i in range(len(list(df_adj))):
    df_adj["Lag_1"+" "+list(df_adj)[i]]=df_adj.iloc[:,i].shift(30)
    
# Lag feature
fig, ax = plt.subplots()
for i in range((len(list(df_adj)))//2):
    name=list(df_adj)[i]
    ax = sns.regplot(x="Lag_1"+" "+name, y=name, data=df_adj)
    ax.set_aspect('equal')
    ax.set_title("30 days Lag Plot of"+" "+name)
    plt.show()
    
    

