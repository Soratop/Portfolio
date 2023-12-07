import yfinance as yf
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import time
import seaborn as sns

# get data
def get_df(list,start_time,end_time):
    df=yf.download(list,start=start_time, end=end_time, interval = "1d").reset_index()
    return df

def data_date(data,start_time,end_time):
    b=pd.DataFrame(pd.date_range(start=start_time,end=end_time,freq='d'),columns=["Date"])
    b=b.reset_index().set_index("Date")
    c=pd.merge(b,data,how="left",on="Date").interpolate()
    c.index=pd.to_datetime(c["Date"])
    c=c[c.index>datetime.datetime(2010,11,30)]
    return c

# show graph
def swap_graph(Df,data_index,xlabel,save_place,save=False,
               title="Swap points per quarterly(Leverage 1x) don't enough 2023/12/01-2023/12/31",
               show=True,
               ro=0,la=40):
    if show:
        fig,ax= plt.subplots(figsize=(18,9))
        ax.plot(data_index,xlabel,data=Df)
        ax.set_xlabel(xlabel,color="red")
        ax.set_ylabel("Swap point(%)",rotation=ro,labelpad=la,color="red")
        ax.set_title(title,color="red")
        if save:
            if save_place==False:
                print("need the setting save file place")
            else:
                plt.savefig(save_place)
        if show:
            plt.show()

# show heatmap
def show_heatmap(Data,saveplace,show=False,save=False):
    if show:
        fig, ax = plt.subplots(figsize=(12, 9)) 
        sns.heatmap(Data,cmap="Reds",vmin=0, vmax=1,annot=True)
    if save==True:
        plt.savefig(saveplace)
    if show:
        plt.show()
        
# read the spap point data
df=pd.read_csv("Swap\lionfx_swap.csv")
swap=df.iloc[:,[0,2]].reset_index().set_index("Date").drop("index",axis=1)

# make the usdjpy
swap=swap.rename(columns={'Unnamed: 2': 'USDJPY'})
# change the base to datetime
swap.index=pd.to_datetime(swap.index)

# calculate swap 
usd_jpy=swap.copy()
usd_jpy=usd_jpy.to_period("Y").groupby("Date").sum()

# change the period to datetime
usd_jpy.index=usd_jpy.index.to_timestamp()

#time
start_time="2008-01-29"
end_time="2023-11-30"

usd_jpy=swap.to_period("d").groupby("Date").sum()
usd_jpy.index=usd_jpy.index.to_timestamp()

df=pd.DataFrame(pd.date_range(start=start_time,end=end_time,freq='d'),columns=["Date"])
df=df.reset_index().set_index("Date")
df.index=pd.to_datetime(df.index)
df=pd.merge(usd_jpy,df,how="right",on="Date").drop("index",axis=1)
df=df.fillna(0)

jpy_x=get_df("JPY=X",start_time,end_time)
b=pd.DataFrame(pd.date_range(start=start_time,end=end_time,freq='d'),columns=["Date"])
b=b.reset_index().set_index("Date")
b.index=pd.to_datetime(b.index)
jpy_x=pd.merge(b,jpy_x,how="left",on="Date").interpolate()

df["Swap"]=0

for i in range(len(df)):
    if df["USDJPY"][i]!=0:
        df["Swap"][i]=(df["USDJPY"][i])/(jpy_x["Adj Close"][i]*1000)*100
        
df_d=df.to_period("d").groupby("Date").sum()
df_q=df.to_period("q").groupby("Date").sum()
df_y=df.to_period("Y").groupby("Date").sum()
df_d.index=df_d.index.to_timestamp()
df_q.index=df_q.index.to_timestamp()
df_y.index=df_y.index.to_timestamp()

# show swap point graph      
swap_graph(show=False,Df=df_q,data_index=df_q.index,xlabel="month",save=False,title="Swap points per quarterly(Leverage 1x) don't enough 2023/12/01-2023/12/31",save_place="Swap_graph/Swap points per quarterly(Leverage 1x).png")
swap_graph(show=False,Df=df_y,data_index=df_y.index,xlabel="year",save=False,title="Swap points per year(Leverage 1x)",save_place='Swap_graph/Swap points per year(Leverage 1x).png')
swap_graph(show=False,Df=df_d,data_index=df_d.index,xlabel="year",save=False,title="Swap points per day(Leverage 1x)",save_place='Swap_graph/Swap points per day(Leverage 1x).png')

# delay 365days
df_d["365days"]=0
for i in range(len(df_d)-364):
    j=i+364
    df_d["365days"][j]=np.cumsum(df_d[i:j]["Swap"]).iloc[-1]

swap_graph(show=False,Df=df_d,data_index=df_d.index,xlabel="365days",save=False,title="Total USD/JPY swap points per 365days(Leverage 1x)",save_place='Swap_graph/Total USD_JPY swap points per 365days.png')

# get data
df_voo=get_df("VOO","2010-11-30","2023-11-30")
voo_date=data_date(df_voo,"2010-11-30","2023-11-30")

df_qqq=get_df("QQQ","2010-11-30","2023-11-30")
qqq_date=data_date(df_qqq,"2010-11-30","2023-11-30")

df_n225=get_df("^N225","2010-11-30","2023-11-30")
n225_date=data_date(df_n225,"2010-11-30","2023-11-30")

jpy_x=get_df("JPY=X","2010-11-30","2023-11-30")
jpy_x_date=data_date(jpy_x,"2010-11-30","2023-11-30")

n225_date["Usd Close"]=0

for i in range(len(n225_date)):
    n225_date["Usd Close"][i]=n225_date["Adj Close"][i]/jpy_x_date["Adj Close"][i]


df_usd=pd.DataFrame({"USDJPY":jpy_x_date["Adj Close"],"VOO":voo_date["Adj Close"],"QQQ":qqq_date["Adj Close"],"N225":n225_date["Usd Close"]})

## Compute pairwise correlation
df_corr= df_usd.corr().round(3)

# show heatmap
show_heatmap(show=True,Data=df_corr,saveplace='Swap_graph/correlation.png')