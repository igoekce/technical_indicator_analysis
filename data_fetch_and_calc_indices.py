import pandas as pd
import yfinance as yf
import ta
import warnings

warnings.filterwarnings('ignore')

# Define the ticker list
tickers_list = ['^NDX', '^IXIC', '^DJI', '^GSPC', '^RUT', '^GDAXI', '^STOXX50E', '^N225', '^HSI', '^NSEI',  '^CMC200', 'GC=F']

# Fetch the data
data = yf.download(tickers_list, '2020-1-1')['Adj Close']

# Create a dataframe to store the adjusted close price of the stocks
df = pd.DataFrame()

# Store the adjusted close price of the stock into the df
for ticker in tickers_list:
    df[ticker] = data[ticker]

# Calculate technical indicators
for ticker in tickers_list:
    # Calculate 50-day Simple Moving Average (SMA)
    df[ticker + "_SMA_50"] = ta.trend.sma_indicator(df[ticker], window=50)

    # Calculate 200-day Simple Moving Average (SMA)
    df[ticker + "_SMA_200"] = ta.trend.sma_indicator(df[ticker], window=200)

    # Calculate Relative Strength Index (RSI)
    df[ticker + "_RSI"] = ta.momentum.rsi(df[ticker], window=14)

    # Calculate Moving Average Convergence Divergence (MACD)
    df[ticker + "_MACD"] = ta.trend.macd_diff(df[ticker])

    # Calculate Bollinger Bands
    bollinger = ta.volatility.BollingerBands(df[ticker])
    df[ticker + "_bollinger_hband"] = bollinger.bollinger_hband()
    df[ticker + "_bollinger_lband"] = bollinger.bollinger_lband()

# Create signals
sentiment = {}

for ticker in tickers_list:
    sentiment[ticker] = {}

    # Calculate trading signals for each indicator
    df[ticker + "_Signal_SMA"] = "Neutral"
    df.loc[df[ticker + "_SMA_50"] > df[ticker + "_SMA_200"], ticker + "_Signal_SMA"] = "Buy"
    df.loc[df[ticker + "_SMA_50"] < df[ticker + "_SMA_200"], ticker + "_Signal_SMA"] = "Sell"
    sentiment[ticker]["Signal_SMA"] = df[ticker + "_Signal_SMA"].iloc[-1]

    df[ticker + "_Signal_RSI"] = "Neutral"
    df.loc[df[ticker + "_RSI"] < 30, ticker + "_Signal_RSI"] = "Buy"
    df.loc[df[ticker + "_RSI"] > 70, ticker + "_Signal_RSI"] = "Sell"
    sentiment[ticker]["Signal_RSI"] = df[ticker + "_Signal_RSI"].iloc[-1]

    df[ticker + "_Signal_MACD"] = "Neutral"
    df.loc[df[ticker + "_MACD"] > 0, ticker + "_Signal_MACD"] = "Buy"
    df.loc[df[ticker + "_MACD"] < 0, ticker + "_Signal_MACD"] = "Sell"
    sentiment[ticker]["Signal_MACD"] = df[ticker + "_Signal_MACD"].iloc[-1]

    df[ticker + "_Signal_BOLLINGER"] = "Neutral"
    df.loc[df[ticker] < df[ticker + "_bollinger_lband"], ticker + "_Signal_BOLLINGER"] = "Buy"
    df.loc[df[ticker] > df[ticker + "_bollinger_hband"], ticker + "_Signal_BOLLINGER"] = "Sell"
    sentiment[ticker]["Signal_BOLLINGER"] = df[ticker + "_Signal_BOLLINGER"].iloc[-1]

# Convert sentiment dictionary to DataFrame
sentiment_df = pd.DataFrame(sentiment).transpose()

# Save sentiment data as a CSV file
sentiment_df.to_csv('data/sentiment_data.csv')
