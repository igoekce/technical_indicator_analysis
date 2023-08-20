import pandas as pd
import yfinance as yf
import ta
import matplotlib.pyplot as plt


import warnings
warnings.filterwarnings('ignore')


# Define the ticker list
tickers_list = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'GOOGL', 'META', 'TSLA', 'NVDA', 'PYPL', 'INTC', 'CMCSA', 'CSCO', 'NFLX', 'ADBE', 'PEP', 'TMUS', 'AMGN', 'COST', 'AVGO', 'QCOM', 'TXN', 'SBUX', 'CHTR', 'AMD', 'GILD', 'BKNG', 'MDLZ', 'MELI', 'LRCX', 'ASML', 'ADP', 'BIDU', 'ISRG', 'CSX', 'INTU', 'BIIB', 'MAR', 'AAL', 'NKE', 'EA', 'REGN', 'FOX', 'FISV', 'ADSK', 'ATVI', 'ILMN', 'EXPE', 'MCHP', 'CTAS', 'IDXX', 'ZM', 'WDAY', 'NTES', 'XLNX', 'KLAC', 'CTSH', 'VRSK', 'NXPI', 'LULU', 'FAST', 'BMRN', 'PAYX', 'ALGN', 'SIRI', 'VRSN', 'PCAR', 'DLTR', 'SWKS', 'CSGP', 'QRTEA', 'SNPS', 'HSIC', 'LBTYA', 'KLIC', 'WDC', 'EXC', 'EXPD', 'AEP', 'WBA', 'VIA.DE', 'CDW', 'XEL', 'ANSS', 'CDNS', 'CTX.DE', 'WTY.F', 'ROST', 'JD', 'ADS.DE', 'ALV', 'BAS.DE', 'BAYN.DE', 'BEI.DE', 'BMW.DE', 'CON', 'MBG.DE', 'DBK.DE', 'DB1.DE', 'DHER.DE', 'DPW.DE', 'DTE', 'DWNI.DE', 'EOAN.DE', 'FRE.DE', 'FME.DE', 'HEI', 'HEN3.DE', 'IFX.DE', 'LIN', 'MTX', 'MUV2.DE', 'RWE.DE', 'SAP', 'SIE.DE', 'VNA.DE', 'VOW3.DE', 'AXP', 'BA', 'CAT', 'CRM', 'CVX', 'DIS', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WMT']


# Fetch the data
data = yf.download(tickers_list,'2020-1-1')['Adj Close']

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
for ticker in tickers_list:
    df[ticker + "_Signal_SMA"] = "Hold"
    df.loc[df[ticker + "_SMA_50"] > df[ticker + "_SMA_200"], ticker + "_Signal_SMA"] = "Buy"
    df.loc[df[ticker + "_SMA_50"] < df[ticker + "_SMA_200"], ticker + "_Signal_SMA"] = "Sell"

    df[ticker + "_Signal_RSI"] = "Hold"
    df.loc[df[ticker + "_RSI"] < 30, ticker + "_Signal_RSI"] = "Buy"
    df.loc[df[ticker + "_RSI"] > 70, ticker + "_Signal_RSI"] = "Sell"

    df[ticker + "_Signal_MACD"] = "Hold"
    df.loc[df[ticker + "_MACD"] > 0, ticker + "_Signal_MACD"] = "Buy"
    df.loc[df[ticker + "_MACD"] < 0, ticker + "_Signal_MACD"] = "Sell"

    df[ticker + "_Signal_BOLLINGER"] = "Hold"
    df.loc[df[ticker] < df[ticker + "_bollinger_lband"], ticker + "_Signal_BOLLINGER"] = "Buy"
    df.loc[df[ticker] > df[ticker + "_bollinger_hband"], ticker + "_Signal_BOLLINGER"] = "Sell"

# ... previous script ...

# Create signals
for ticker in tickers_list:
    df[ticker + "_Signal_SMA"] = 0
    df.loc[df[ticker + "_SMA_50"] > df[ticker + "_SMA_200"], ticker + "_Signal_SMA"] = 1
    df.loc[df[ticker + "_SMA_50"] < df[ticker + "_SMA_200"], ticker + "_Signal_SMA"] = -1

    df[ticker + "_Signal_RSI"] = 0
    df.loc[df[ticker + "_RSI"] < 30, ticker + "_Signal_RSI"] = 1
    df.loc[df[ticker + "_RSI"] > 70, ticker + "_Signal_RSI"] = -1

    df[ticker + "_Signal_MACD"] = 0
    df.loc[df[ticker + "_MACD"] > 0, ticker + "_Signal_MACD"] = 1
    df.loc[df[ticker + "_MACD"] < 0, ticker + "_Signal_MACD"] = -1

    df[ticker + "_Signal_BOLLINGER"] = 0
    df.loc[df[ticker] < df[ticker + "_bollinger_lband"], ticker + "_Signal_BOLLINGER"] = 1
    df.loc[df[ticker] > df[ticker + "_bollinger_hband"], ticker + "_Signal_BOLLINGER"] = -1


# Sum the signals for each day
for ticker in tickers_list:
    df[ticker + '_Sum_Buy'] = df[[ticker + strategy for strategy in ["_Signal_SMA", "_Signal_RSI", "_Signal_MACD", "_Signal_BOLLINGER"]]].clip(lower=0).sum(axis=1)
    df[ticker + '_Sum_Hold'] = df[[ticker + strategy for strategy in ["_Signal_SMA", "_Signal_RSI", "_Signal_MACD", "_Signal_BOLLINGER"]]].eq(0).sum(axis=1)
    df[ticker + '_Sum_Sell'] = df[[ticker + strategy for strategy in ["_Signal_SMA", "_Signal_RSI", "_Signal_MACD", "_Signal_BOLLINGER"]]].clip(upper=0).abs().sum(axis=1)

# Define a new DataFrame to store the counts
counts_df = pd.DataFrame()

# Add the counts to the new DataFrame
for ticker in tickers_list:
    counts_df[ticker + '_Buy'] = df[ticker + '_Sum_Buy']
    #counts_df[ticker + '_Hold'] = df[ticker + '_Sum_Hold']
    counts_df[ticker + '_Sell'] = df[ticker + '_Sum_Sell']

# Get the last 60 days of data
counts_df_60 = counts_df.tail(60)

# Filter columns where the count is 3 or more for any of the latest 5 days
#filtered_columns = counts_df_60.tail(5).ge(3).any()

# Apply the filter to the DataFrame
#filtered_df_1 = counts_df_60.loc[:, filtered_columns]

# Save the DataFrame to a CSV file
#filtered_df_1.to_csv('data/filtered_df_1.csv', index=True)
counts_df_60.to_csv('data/filtered_df_1.csv', index=True)