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

def read_csv(path, index_col, use_cols):
    """Read excel file base on the file path and index col and returns the data frame."""
    return pd.read_csv(path, index_col = index_col, parse_dates = [index_col], usecols=use_cols)

data = read_csv(
    r"C:\Users\Dell G3 3590\OneDrive\StockData\SPY.csv",
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

def plot_graph(data, legends, xLabel="", yLabel=""):
    """Plot the a graph base on the params."""
    plt.plot(data)
    plt.legend(legends)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    
#plot_graph(data[stockDataKeys], stockDataKeys, "Time", "Price")
#plot_graph(data[strategyDataKeys], strategyDataKeys, "Time", "Return")

spyData = read_csv(
    r"C:\Users\Dell G3 3590\OneDrive\StockData\SPY.csv",
    dateKey, 
    [dateKey, closeKey]
    ).pct_change()

aaplData = read_csv(
    r"C:\Users\Dell G3 3590\OneDrive\StockData\aapl.csv",
    dateKey, 
    [dateKey, closeKey]
    ).pct_change()

corData = spyData.rolling(50).corr(aaplData)[-200:]
plot_graph(corData, ["AAPL and SPY cor"])

"""
import backtrader as bt

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
"""