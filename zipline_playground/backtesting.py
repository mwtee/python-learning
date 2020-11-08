from zipline import run_algorithm
from zipline.api import order_target_percent, order_target, symbol, record
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import pandas as pd


def initialize(context):
    context.stock = symbol("AAPL")
    context.index_average_window = 100


def handle_data(context, data):
    # Request history for the stock
    equities_hist = data.history(
        context.stock,
        "close",
        context.index_average_window,
        "1d")

    # Compute averages
    short_mavg = data.history(context.stock, 'price', bar_count=20, frequency="1d").mean()
    long_mavg = data.history(context.stock, 'price', bar_count=50, frequency="1d").mean()

    # Trading logic
    if short_mavg > long_mavg:
        order_target(context.stock, 100)
    elif short_mavg < long_mavg:
        order_target(context.stock, 0)

    # Save values for later inspection
    record(AAPL=data.current(context.stock, 'price'),
           short_mavg=short_mavg,
           long_mavg=long_mavg)


def analyze(context, perf):
    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(211)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value in $')

    ax2 = fig.add_subplot(212)
    perf['AAPL'].plot(ax=ax2)
    perf[['short_mavg', 'long_mavg']].plot(ax=ax2)

    perf_trans = perf.loc[[t != [] for t in perf.transactions]]
    buys = perf_trans.loc[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
    sells = perf_trans.loc[
        [t[0]['amount'] < 0 for t in perf_trans.transactions]]
    ax2.plot(buys.index, perf.short_mavg.loc[buys.index],
             '^', markersize=10, color='m')
    ax2.plot(sells.index, perf.short_mavg.loc[sells.index],
             'v', markersize=10, color='k')
    ax2.set_ylabel('price in $')
    plt.legend(loc=0)
    plt.show()

    # fig = plt.figure(figsize=(12, 8))

    # ax = fig.add_subplot(311)
    # ax.set_title("Strategy Results")
    # ax.semilogy(perf["portfolio_value"], linestyle="-", label="Equity curve", linewidth=3.0)
    # ax.legend()
    # ax.grid(False)

    # ax = fig.add_subplot(312)
    # ax.plot(
    #     perf["gross_leverage"],
    #     label="Exposure",
    #     linestyle="-",
    #     linewidth=1.0)
    # ax.legend()
    # ax.grid(True)

    # ax = fig.add_subplot(313)
    # ax.plot(perf["returns"], label="Returns", linestyle="-", linewidth=1.0)
    # ax.legend()
    # ax.grid(True)


start_date = pd.Timestamp('2017-09-1', tz='utc')
end_date = pd.Timestamp('2018-03-31', tz='utc')
type(start_date)

results = run_algorithm(
    start=start_date,
    end=end_date,
    initialize=initialize,
    analyze=analyze,
    handle_data=handle_data,
    capital_base=100000,
    data_frequency="daily",
    bundle="quandl")
