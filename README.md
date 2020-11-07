# python-learning
Exploring python for finance

All projects setup assumes you have Anaconda installed

## Setup
### Panda, numpy and pyplot playground
1) Run main.py
2) Follow the menu options to explore the functionality

### zipline_playground
1) Setup python env to use python 3.6
2) Run `conda install -c Quantopian zipline` to install zipline library
3) Register a Quandl account to get your API key for stock data
4) Run `Set QUANDL_API_KEY=your_api_key` to set the env key for Windows. Mac may be `export QUANDL_API_KEY=your_api_key`
5) Run `zipline ingest -b quandl` to download the free stock data
6) Run `backtesting.py`
