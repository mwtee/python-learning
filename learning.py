import pandas as pd
import numpy as np

#stocks = {
#"CAKE": "Cheesecake Factory",
#"PZZA": "Papa John's Pizza"
#}

#for ticker, name in stocks.items():
 #   print("{} has ticker {}".format(name, ticker))
    
dateKey = "Date"
closeKey = "Close"
sma50Key = "SMA50"
sma100Key = "SMA100"
    
data = pd.read_excel(
    r"C:\Users\Dell G3 3590\OneDrive\sp500_2009_2020.xlsx", 
    index_col=dateKey, 
    parse_dates=[dateKey],
    usecols=[dateKey, closeKey]
)

data[sma50Key] = data[closeKey].rolling(50).mean()
data[sma100Key] = data[closeKey].rolling(100).mean()

data.plot()