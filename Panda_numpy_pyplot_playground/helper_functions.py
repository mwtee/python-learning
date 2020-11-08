import pandas as pd
import matplotlib.pyplot as plt


def read_csv(path, index_col, use_cols):
    """Read excel file base on the file path and index col and returns the data frame."""
    return pd.read_csv(path, index_col=index_col, parse_dates=[index_col], usecols=use_cols)


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
    plt.show()
