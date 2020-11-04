#
# Copyright 2013 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logbook

import pandas as pd

log = logbook.Logger(__name__)


def get_benchmark_returns_from_file(filelike):
    """
    Get a Series of benchmark returns from a file

    Parameters
    ----------
    filelike : str or file-like object
        Path to the benchmark file.
        expected csv file format:
        date,return
        2020-01-02 00:00:00+00:00,0.01
        2020-01-03 00:00:00+00:00,-0.02

    """
    log.info("Reading benchmark returns from {}", filelike)

    df = pd.read_csv(
        filelike,
        index_col=['date'],
        parse_dates=['date'],
    ).tz_localize('utc')

    if 'return' not in df.columns:
        raise ValueError("The column 'return' not found in the "
                         "benchmark file \n"
                         "Expected benchmark file format :\n"
                         "date, return\n"
                         "2020-01-02 00:00:00+00:00,0.01\n"
                         "2020-01-03 00:00:00+00:00,-0.02\n")

    return df['return'].sort_index()

from zipline import run_algorithm
from zipline.api import order_target_percent, symbol
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
    
    if equities_hist[-1] > equities_hist.mean():
        stock_weight = 1.0
    else:
        stock_weight = 0.0
        
    order_target_percent(context.stock, stock_weight)
    
def analyze(context, perf):
    fig = plt.figure(figsize=(12, 8))
    
    ax = fig.add_subplot(311)
    ax.set_title("Strategy Results")
    ax.semilogy(perf["portfolio_value"], linestyle="-", label="Equity curve", linewidth=3.0)
    ax.legend()
    ax.grid(False)
    
    ax = fig.add_subplot(312)
    ax.plot(
        perf["gross_leverage"],
        label="Exposure",
        linestyle="-",
        linewidth=1.0)
    ax.legend()
    ax.grid(True)
    
    ax = fig.add_subplot(313)
    ax.plot(perf["returns"], label="Returns", linestyle="-", linewidth=1.0)
    ax.legend()
    ax.grid(True)
    
    
start_date = pd.Timestamp('2017-1-1', tz='utc')
end_date = pd.Timestamp('2018-03-31', tz='utc')
type(start_date)

results = run_algorithm(
    start=start_date,
    end=end_date,
    initialize=initialize, 
    analyze=analyze,
    handle_data=handle_data,
    capital_base=100000,
    data_frequency = "daily",
    bundle="quandl")
