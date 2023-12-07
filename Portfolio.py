from portfolio_backtest import Backtest
import pprint
import yfinance as yf
import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Portfolio list
# USD
US_tickers=["VOO","SPXL"]
Gold=["GC=F"]
Oil=["CL=F"]
USD_tickers= US_tickers

# JPY
JP_tickers=["^N225"]

#Time
Today = pd.to_datetime(datetime.date.today())
Start_time="2011-01-01"
Today= Today.strftime('%Y-%m-%d')

#Get deta
df = yf.download(USD_tickers,start=Start_time, end=Today, interval = "1d").reset_index()    
df.to_csv("Data\yf_list.csv")
df = pd.concat([df["Date"],df["Adj Close"]],axis=1)

for i in USD_tickers:
    msft =yf.Ticker(i)
    msft=msft.dividends
    # msft ~~~ class 'pandas.core.series.Series ~~~
    msft=msft.reset_index()
    msft.to_csv("Data\dividends_" +str(i) + ".csv")

# Interpolation
day= pd.DataFrame(pd.date_range(start=Start_time,end=Today,freq='d'),columns=["Date"])
df=pd.merge(df,day, how = "right").interpolate()
df.to_csv('Portfolio list.csv')
df=df.fillna(method='bfill')
total_days=df["Date"].count()

# Compute pairwise correlation
df_corr= df.drop(["Date"],axis=1).corr().round(3)

# heatmap
fig, ax = plt.subplots(figsize=(12, 9)) 
sns.heatmap(df_corr,cmap="Reds",vmin=0, vmax=1,annot=True)
plt.savefig('correlation.png')

# Leverage
df_d_voo=pd.read_csv("Data\dividends_VOO.csv")
df_d_spxl=pd.read_csv("Data\dividends_SPXL.csv")
Total_Remainder="VOO_75%+Spxl_25%"
df_ex=df.copy()
df_ex["Total"]=0
df_ex[Total_Remainder]=0
df_ex["Stock"]=0
df_ex["Remainder"]=0
df_ex["Have_voo"]=0
df_ex["Have_spxl"]=0
df_ex["Voo_%"]=0
df_ex["Spxl_%"]=0
df_ex["Voo_100%"]=0
df_ex["Spxl_100%"]=0
Money=10000

for i in range(total_days):
    if i==0:
        i_m=10000
        i_voo_p=df["VOO"][i]
        i_spxl_p=df["SPXL"][i]
    
    #now price
    Voo_p=df["VOO"][i]
    Spxl_p=df["SPXL"][i]
    
    # Total Money
    if i!=0:
        Money=(B_voo*Voo_p)+(B_spxl*Spxl_p)+Remainder
        
    
    # Buy voo ,spxl and then remainder of buying voo and spxl
    B_voo=(Money*0.75)//Voo_p
    M_voo=B_voo*Voo_p
    B_spxl=(Money-M_voo)//Spxl_p
    M_spxl=B_spxl*Spxl_p
    Remainder=Money-(M_spxl+M_voo)
    
    df_ex["Total"][i]=Money
    df_ex[Total_Remainder][i]=Money+Remainder
    df_ex["Stock"][i]=M_voo+M_spxl
    df_ex["Remainder"][i]=Remainder
    df_ex["Have_voo"][i]=M_voo
    df_ex["Have_spxl"][i]=M_spxl
    df_ex["Voo_%"][i]=((M_voo)/Money).round(3)
    df_ex["Spxl_%"][i]=((M_spxl)/Money).round(3)
    df_ex["Voo_100%"][i]=i_m*(Voo_p/i_voo_p)
    df_ex["Spxl_100%"][i]=i_m*(Spxl_p/i_spxl_p)
    
df_ex.to_csv("df_ex.csv")

# add button graph
fig = make_subplots(rows=1, cols=1)

print(df_ex[Total_Remainder])
for i, j in enumerate([df_ex[Total_Remainder],df_ex["Voo_100%"],df_ex["Spxl_100%"]]):
    fig.add_trace(go.Scatter(x=df_ex["Date"].unique(), y=j,name=j.name))
    
fig.update_xaxes(rangeslider_visible=True,
                 rangeselector=dict(
                     buttons=list([
                         dict(count=6, label="6m", step="month", stepmode="backward"),
                         dict(count=1, label="1y", step="year", stepmode="backward"),
                         dict(count=2, label="2y", step="year", stepmode="backward"),
                         dict(count=2, label="3y", step="year", stepmode="backward"),
                         dict(count=2, label="5y", step="year", stepmode="backward"),
                         dict(count=2, label="10y", step="year", stepmode="backward"),
                         dict(step="all")])),
                 row=1,col=1)
fig.show()

#print(df)
#Day_return =df.pct_change()
#print(Day_return)

# cumulative sum
#cum_return=1+df.pct_change().cumprod()
#cum_return.iloc[0,:] = 1
#x=df["Date"].reset_index().iloc[:,1]
#print(list(x))
#y=cum_return
#plt.plot(x,y)
#plt.plot(x,y,figsize=(12,8))
#plt.savefig('Returns.png')
#cum_return.to_csv('Returns.csv')



#d_v_count,d_s_count=0,0
#d_v=[]
#d_s=[]
#i_v=0
#i_s=0
#c_v=0
#c_s=0
#f_v=False
#f_s=False
#r,k=0,0
#for i in list(df_d_voo["Date"]):
    #for j in list(df_ex["Date"]):
        #if i[:10]==str(j)[:10]:
            #d_v.append(i[:10])
    
#for i in list(df_d_spxl["Date"]):
   # for j in list(df_ex["Date"]):
       # if i[:10]==str(j)[:10]:
           # d_s.append(i[:10])

#print(d_s)
    #dividends 
    #print(str(d_v[i_v]),str(df_ex["Date"][i])[:10])
    #if (i!=0) and (str(d_v[i_v]) == str(df_ex["Date"][i])[:10]):
        #f_v=True
    #print(str(d_s[i_s]),f_s,c_s)    
    #if (i!=0) and (str(d_s[i_s]) == str(df_ex["Date"][i])[:10]):
        #f_s=True
            
    #if f_v==True:
       # c_v+=1
    
    #if# f_s==True:
        #c_s+=1
        
    #if 3c_v==2:
        #Money+=df_d_voo["Dividends"][i_v]*B_voo
        #r+=df_d_voo["Dividends"][i_v]*B_voo
        #c_v=0
        #i_v+=1
        #f_v==False
        
    #if #c_s==2:
        #Money+=df_d_spxl["Dividends"][i_s]*B_spxl
        #k+=df_d_spxl["Dividends"][i_s]*B_spxl
        #c_s=0
        #i_s+=1
        #f_s==False
        

# no button graph
#a=pd.concat([df_ex[Total_Remainder],df_ex["Voo_100%"],df_ex["Spxl_100%"],df_ex["Date"]],axis=1).reset_index()
#fig=px.line(a, x="Date", y=[Total_Remainder,"Voo_100%","Spxl_100%"] )
#fig.show()



# Check for missing values.
#Check_Nan=False

#if Check_Nan==True:
   # print("Count the Nan")
    #print(df.isnull().sum())

# Interpolation
#if Check_Nan==True:
    #print("After interpolating")
    #print(df.isnull().sum())
    
# drawdown
#Drawdown_list=["Max drawdown"]
#for i in range(len(list(Df_adj_close))):
    #Drawdown=1
    #Drawdown_percent=1
    #List_name=list(Df_adj_close)[i]
    #a=Df_adj_close.iloc[:,i]
    #for j in range(Total_days):
        #if a[j] != "NaN":
            #p=float(a[j])
            #Drawdown=max(Drawdown,p)
            #Drawdown_percent=max(Drawdown_percent,((Drawdown-p)*100/Drawdown))
    #Drawdown_list.append([str(List_name)+" "+str(round(Drawdown_percent,3))+"%"])
        

# Leverage
#Leverage_flag=False
#Money_now=Df_adj_close["VOO"]
#Money_now=Df_adj_close["VOO"].weekday()
#print(Money_now)
#for i in range(Total_days):
    #if Df_adj_close[i]==Df_adj_close[i+]:

#if Leverage_flag==True:
   # Leverage=Df_adj_close*1.5
    #L_list=[]
    ##for i in range(len(list(Leverage))):
      #  L_list.append("L1.5"+list(Leverage)[i])
        
    #Leverage=Leverage.set_axis(L_list,axis=1)
    #Df_adj_close=pd.concat([Df_adj_close,Leverage],axis=1)



# Day return
#Day_return=1+df.pct_change()

# cumulative sum
#cum_return=1+df.pct_change().cumprod()
#cum_return.iloc[0,:] = 1
#x=df["Date"].reset_index().iloc[:,1]
#print(list(x))
#y=cum_return
#plt.plot(x,y)
#plt.plot(x,y,figsize=(12,8))
#plt.savefig('Returns.png')
#cum_return.to_csv('Returns.csv')

#plt.show()

#Data=Backtest(tickers= USD_tickers,start=Start_time,end=Today).run()

#Portfolio=10*6
#Portofolio_leverage=1.5
#L_voo=0.75
#L_spxl=0.25

#df["Total_money"]=0
#df["Total_stock"]=0
#df["Remainder"]=0
#df["Count_voo"]=0
#df["Money_voo"]=0
#df["Count_spxl"]=0
#df["Money_spxl"]=0
#Df_adj_close["Voo_%"]=0
#Df_adj_close["Spxl_%"]=0
#df["Only_buy_voo"]=0
#df["Only_buy_spxl"]=0

#print(Df_adj_close.loc[pd.date_range(start=Start_time,end=Today,freq='m'),:])
#df_day=pd.date_range(start=Start_time,end=Today,freq='m')
#Buy_Voo=0
#Buy_Spxl=0
#Cost=0
#Money=10000
#Buy_flag=True
#Df_voo=df["VOO"]
#Df_Spxl=df["SPXL"]
#print(Df_adj_close["VOO"].reset_index().iloc[0,1])
#print(Df_adj_close["Buy_voo"])
#print(Df_adj_close["Buy_voo"].reset_index().iloc[0,1])
#for i in range(2):
    #if i==0:
        #initial_money=Money
        #initial_voo_price=Df_voo.iloc[0,1]
        #initial_spxl_price=Df_Spxl.iloc[0,1]
        #Voo_price=0
        #Spxl_price=0
        
    #Yesterday price
    #Before_voo_price=Voo_price
    #Before_spxl_price=Spxl_price
    
    #now price
    #Voo_price=Df_voo.iloc[i,1]
    #Spxl_price=Df_Spxl.iloc[i,1]
    
    # Total Money
    #if i!=0:
        #Money=(Voo_price*Buy_voo)+(Money_spxl*Buy_spxl)
    
    # Buy voo ,spxl and then remainder of buying voo and spxl
    #Buy_spxl=(Money*L_spxl)//Spxl_price
    #Money_spxl=Buy_spxl*Spxl_price
    #Buy_voo=(Money-Money_spxl)//Voo_price
    #Money_voo=Buy_voo*Voo_price
    #Remainder=Money-(Money_spxl+Money_voo)
    
    # writing data
    #day=df.iloc[i,]
    #df.loc[i,"Count_voo"]=Money_voo
    #df.loc[i,"Count_spxl"]=Money_spxl
    #df.loc[i,"Total_stock"]=Money_voo+Money_spxl
    #df.loc[i,"Remainder"]=Remainder
    #df.loc[i,"Total_money"]=Money
    #Df_adj_close.loc[i,"Only_buy_voo"]=(cum_return["VOO"].reset_index().iloc[i,1])*(initial_money//initial_voo_price)
    #Df_adj_close.loc[i,"Only_buy_spxl"](cum_return["SPXL"].reset_index().iloc[i,1])*(initial_money//initial_spxl_price)
    
    
    #Df_adj_close["Count_spxl"].reset_index().iloc[i,1]=Money_spxl
    #Df_adj_close["Total_stock"].reset_index().iloc[i,1]=Money_voo+Money_spxl
    #Df_adj_close["Remainder"].reset_index().iloc[i,1]=Remainder
    #Df_adj_close["Total_money"]=Money
    #Df_adj_close["Only_buy_voo"].reset_index().iloc[i,1]=(cum_return["VOO"].reset_index().iloc[i,1])*(initial_money//initial_voo_price)
    #Df_adj_close["Only_buy_spxl"].reset_index().iloc[i,1]=(cum_return["SPXL"].reset_index().iloc[i,1])*(initial_money//initial_spxl_price)


#df.to_csv('Df_adj_close.csv')
#df=pd.merge(df["Total_stock"],df["Only_buy_Voo"],df["Only_buy_spxl"])
#df.plot(figsize=(12,8))
#plt.show()
    
    
    
    
    #Before_total_money=Before_voo_price+Before_spxl_price
    #Money=(Before_total_money)+(Voo_price+Spxl_price-Before_total_money)
    
    #if i==0:
        #Df_adj_close["Buy_voo"].reset_index().iloc[i,1]=Voo_price*(Money*L_voo)
        #Df_adj_close["Buy_spxl"].reset_index().iloc[i,1]=Spxl_price*(Money*L_spxl)
        #Df_adj_close["Buy_stock"].reset_index().iloc[i,1]=Voo_price+Spxl_price
        #Money=Df_adj_close["Buy_stock"].reset_index().iloc[i,1]
        
    #elif Df_adj_close.loc[df_day,:]:
        #Money=Df_adj_close["Buy_stock"].reset_index().iloc[i,1]
        #Df_adj_close["Buy_voo"].reset_index().iloc[i,1]=Voo_price*(Money*L_voo)
        #Df_adj_close["Buy_spxl"].reset_index().iloc[i,1]=Spxl_price*(Money*L_spxl)
        #Df_adj_close["Total_money"].reset_index().iloc[i,1]=Voo_price+Spxl_price
        
   # Money=Df_adj_close["Total_money"].reset_index().iloc[i,1]
    #Df_adj_close["Voo_%"].reset_index().iloc[i,1]=Df_adj_close["Buy_voo"].reset_index().iloc[i,1]/(Df_voo.iloc[i,1]+Df_Spxl.iloc[i,1])
    #Df_adj_close["Spxl_%"].reset_index().iloc[i,1]=Df_adj_close["Total_money"].reset_index().iloc[i,1]/(Df_voo.iloc[i,1]+Df_Spxl.iloc[i,1])
   
    #if Buy_flag==True:
        #a=(Have_Voo-[Money*L_voo])*Df_adj_close["VOO"].iloc[i,1]
        #b=(Have_Spxl*100-[Money*100*L_voo])
        
        #Voo=Df_adj_close.iloc[i,2]
        #Get_Voo_price
        #Get_Voo_price=Df_adj_close.loc[pd.date_range[i,"VOO"]]
    #Get_Spxl_price=Df_adj_close.loc[pd.date_range[i,"SPXL"]]
    
    #get_money=max((get_Voo_price-Voo_price)*3+(get_Spxl_price-Spxl_price)
    #AVoo_price,Spxl_price=max()
        


# print
#print(list(US_tickers))
#print(Start_time,Today)
#print(list(Drawdown_list))
#print("Return per 1 year" )
#print((Day_return.mean()-1)*365)
    

