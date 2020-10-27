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

def calculate_corr(series1, series2, window):
    """
    Calculate correlation between two series.
    Parameters
    ----------
    series1: DataFrame
    series2: DataFrame
    window: Int

    Returns
    -------
    DataFrame
    """
    ret1 = series1.pct_change()
    ret2 = series2.pct_change()
    return ret1.rolling(window).corr(ret2)

def plot_graph(data, legends, xLabel="", yLabel=""):
    """Plot the a graph base on the params."""
    plt.plot(data)
    plt.legend(legends)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

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
spyData["Spy_Rebased"] = (spyData[-points_to_plot:]["Close"].pct_change() + 1).cumprod()
aaplData["AAPL_Rebased"] = (aaplData[-points_to_plot:]["Close"].pct_change() + 1).cumprod()

corData = spyData.rolling(50).corr(aaplData)[-200:]
plot_graph(corData, ["AAPL and SPY cor"])

