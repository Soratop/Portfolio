import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pyodide.http import open_url

def show_heatmap(Data,saveplace,show=False,save=False):
    if show:
        fig, ax = plt.subplots(figsize=(12, 9)) 
        sns.heatmap(Data,cmap="Reds",vmin=0, vmax=1,annot=True)
    if save==True:
        plt.savefig(saveplace)
    if show:
        plt.show()
        
def set_data():
    url = 
    df = pd.read_csv(open_url(url))
    voo_date=pd.read_csv("D:\Portfolio\html\Data\Voo_date.csv")
    qqq_date=pd.read_csv("html\Data\Qqq_date.csv")
    jpy_x_date=pd.read_csv("html\Data\Jpy_x_date.csv")
    n225_date=pd.read_csv("html\Data\Japan_date.csv")
    n225_date["Usd Close"]=0
    for i in range(len(n225_date)):
        n225_date["Usd Close"][i]=n225_date["Adj Close"][i]/jpy_x_date["Adj Close"][i]
    df_usd=pd.DataFrame({"USDJPY":jpy_x_date["Adj Close"],"VOO":voo_date["Adj Close"],"QQQ":qqq_date["Adj Close"],"N225":n225_date["Usd Close"]})
    df_corr= df_usd.corr().round(3)
    show_heatmap(show=True,Data=df_corr,saveplace='Swap_graph/correlation.png')
    
print(set_data())

