from helper_functions import read_csv, calculate_corr, plot_graph
from constants import dateKey, closeKey, sma50Key, sma100Key, positionKey, strategyKey, strategyPctKey, buyHoldKey

import numpy as np
    
def plot_stock_with_sma():
    data = read_csv(
        r"StockData\SPY.csv",
        dateKey, 
        [dateKey, closeKey]
    )

    data[sma50Key] = data[closeKey].rolling(50).mean()
    data[sma100Key] = data[closeKey].rolling(100).mean()
    
    stockDataKeys = [closeKey, sma50Key]
    plot_graph(data[stockDataKeys], stockDataKeys, "Time", "Price")
    
def plot_sma_crossover_vs_buy_and_hold_strategy_comparison():
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

    strategyDataKeys = [strategyKey, buyHoldKey]
    plot_graph(data[strategyDataKeys], strategyDataKeys, "Time", "Returns")

def plot_correlation(stock_one_ticker, stock_two_ticker):
    spyData = read_csv(
        r"StockData\%s.csv" % (stock_one_ticker),
        dateKey, 
        [dateKey, closeKey]
        )
    
    aaplData = read_csv(
        r"StockData\%s.csv" % (stock_two_ticker),
        dateKey, 
        [dateKey, closeKey]
        )
    
    corData = calculate_corr(spyData, aaplData, 50)[-100:]
    
    plot_graph(corData, ["%s and %s cor" % (stock_one_ticker, stock_two_ticker)])

def work_in_progress(stock_one_ticker, stock_two_ticker):
    spyData = read_csv(
        r"StockData\%s.csv" % (stock_one_ticker),
        dateKey, 
        [dateKey, closeKey]
        )
    
    aaplData = read_csv(
        r"StockData\%s.csv" % (stock_two_ticker),
        dateKey, 
        [dateKey, closeKey]
        )
    points_to_plot = 300
    spyData["Spy_Rebased"] = (spyData[-points_to_plot:][closeKey].pct_change() + 1).cumprod()
    aaplData["AAPL_Rebased"] = (aaplData[-points_to_plot:][closeKey].pct_change() + 1).cumprod()
    
def print_menu():
    print(22 * "-" , "Ming's Algo Learning" , 22 * "-")
    print("1. SPY with SMA")
    print("2. SMA crossover strategy backtest")
    print("3. AAPL and SPY price correlation")
    print("Q. Exit")
    print(66 * "-")
    
loop=True

while loop:          ## While loop which will keep going until loop = False
    print_menu()    ## Displays menu
    choice = input("Enter your choice [1-3] or Q: ")
    print("Option %s" % (choice) + " selected")
    
    if choice == '1':     
        ## You can add your code or functions here
        plot_stock_with_sma()
        loop=False
    elif choice == '2':
        plot_sma_crossover_vs_buy_and_hold_strategy_comparison()
        loop=False
    elif choice == '3':
        plot_correlation("SPY", "AAPL")
        loop=False
    elif choice in ('Q', 'q'):
        print("Exiting...")
        loop=False
    else:
        print("Invalid option selection. Please try again..")