import quandl as q
import matplotlib.pyplot as plt
import mplfinance
import matplotlib.dates as mpl_dates
from mplfinance.original_flavor import candlestick_ohlc

def isSupport(df,i):
  support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
  return support

def isResistance(df,i):
  resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
  return resistance

def plot_graph(data, legends, xLabel="", yLabel=""):
    """Plot the a graph base on the params."""
    plt.plot(data)
    plt.legend(legends)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.show()

q.ApiConfig.api_key = "8cH-mQrgu9ne3y1u26y_"
data = q.get("EOD/MSFT", start_date="2013-09-03", end_date="2014-09-30")

data["Date"] = data.index
data["sma20"] = data["Close"].rolling(20).mean()

filteredData = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

levels = []
for i in range(2, filteredData.shape[0]-2):
  if isSupport(data, i):
    levels.append((i, filteredData['Low'][i]))
  elif isResistance(data, i):
    levels.append((i, filteredData['High'][i]))

plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)

# mplfinance.plot(filteredData, type="candle", volume=True, mav=(3, 6, 9))

fig, ax = plt.subplots()

for level in levels:
    plt.plot(data["High"])
    plt.plot(data["Low"])
    plt.hlines(level[1],xmin=data['Date'][level[0]], xmax=max(data['Date']),colors='blue')

fig.show()

def plot_all():
  fig, ax = plt.subplots()
  # candlestick_ohlc(ax, filteredData.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
  # date_format = mpl_dates.DateFormatter('%d %b %Y')
  # ax.xaxis.set_major_formatter(date_format)
  # fig.autofmt_xdate()
  # fig.tight_layout()
  # for level in levels:
  #   plt.hlines(level[1],xmin=data['Date'][level[0]],\
  #              xmax=max(data['Date']),colors='blue')
  # fig.show()


plot_all()