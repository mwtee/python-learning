from helper_functions import read_csv, calculate_corr, plot_graph
from constants import dateKey, closeKey, sma50Key, sma100Key, positionKey, strategyKey, strategyPctKey, buyHoldKey

import numpy as np
    
data = read_csv(
    r"StockData\SPY.csv",
    dateKey, 
    [dateKey, closeKey]
    )

data[sma50Key] = data[closeKey].rolling(50).mean()
data[sma100Key] = data[closeKey].rolling(100).mean()

data[positionKey] = np.where(data[sma50Key] > data[sma100Key], 1, 0)
data[positionKey] = data[positionKey].shift(1)

data[strategyPctKey] = data[closeKey].pct_change(1) * data[positionKey]
data[strategyKey] = (data[strategyPctKey] + 1).cumprod()
data[buyHoldKey] = (data[closeKey].pct_change(1) + 1).cumprod()

stockDataKeys = [closeKey, sma50Key]
strategyDataKeys = [strategyKey, buyHoldKey]
    
#plot_graph(data[stockDataKeys], stockDataKeys, "Time", "Price")
#plot_graph(data[strategyDataKeys], strategyDataKeys, "Time", "Return")

spyData = read_csv(
    r"StockData\SPY.csv",
    dateKey, 
    [dateKey, closeKey]
    )

aaplData = read_csv(
    r"StockData\aapl.csv",
    dateKey, 
    [dateKey, closeKey]
    )

corData = calculate_corr(spyData, aaplData, 50)[-200:].cumprod()

points_to_plot = 300
spyData["Spy_Rebased"] = (spyData[-points_to_plot:][closeKey].pct_change() + 1).cumprod()
aaplData["AAPL_Rebased"] = (aaplData[-points_to_plot:][closeKey].pct_change() + 1).cumprod()

corData = spyData.rolling(50).corr(aaplData)[-200:]
plot_graph(corData, ["AAPL and SPY cor"])

