import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
    
dateKey = "Date"
closeKey = "Close"
sma50Key = "SMA50"
sma100Key = "SMA100"
positionKey = "position"
strategyKey = "Strategy"
strategyPctKey = "StrategyPct"
buyHoldKey = "BuyHold"

data = pd.read_excel(
    r"C:\Users\Dell G3 3590\OneDrive\sp500_2009_2020.xlsx", 
    index_col=dateKey, 
    parse_dates=[dateKey],
    usecols=[dateKey, closeKey]
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

def plot_graph(data, legends, xLabel="", yLabel=""):
    plt.plot(data)
    plt.legend(legends)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    
plot_graph(data[stockDataKeys], stockDataKeys, "Time", "Price")

#plot_graph(data[strategyDataKeys], strategyDataKeys, "Time", "Return")
    
#plt.plot(data[keysForPlotting])
#plt.legend(keysForPlotting)

"""
import backtrader as bt

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
"""