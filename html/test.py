import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pyodide.http import open_url
     

url = "https://raw.githubusercontent.com/Soratop/Portfolio/main/html/Data/df_usd.csv"
df_usd = pd.read_csv(open_url(url))
display(df_usd, target="result")
df_corr= df_usd.corr().round(3)
fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(df_corr,cmap="Reds",vmin=0, vmax=1,annot=True)
#display(fig, target="result")

