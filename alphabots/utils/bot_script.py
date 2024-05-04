import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import copy
import json

def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()
    n = len(df)/12
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR

def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    vol = df["mon_ret"].std() * np.sqrt(12)
    return vol

def sharpe(DF,rf):
    "function to calculate sharpe ratio ; rf is the risk free rate"
    df = DF.copy()
    sr = (CAGR(df) - rf)/volatility(df)
    return sr
    

def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd

# function to calculate portfolio return iteratively
def pflio(DF,m,x):
    """
    Returns cumulative portfolio return
    DF = dataframe with monthly return info for all stocks
    m = number of stock in the portfolio
    x = number of underperforming stocks to be removed from portfolio monthly
    """
    df = DF.copy()
    portfolio = []
    monthly_ret = [0]
    for i in range(len(df)):
        if len(portfolio) > 0:
            monthly_ret.append(df[portfolio].iloc[i,:].mean())
            bad_stocks = df[portfolio].iloc[i,:].sort_values(ascending=True)[:x].index.values.tolist()
            portfolio = [t for t in portfolio if t not in bad_stocks]
        fill = m - len(portfolio)
        new_picks = df.iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
        portfolio = portfolio + new_picks
    monthly_ret_df = pd.DataFrame(np.array(monthly_ret),columns=["mon_ret"])
    return monthly_ret_df

def get_bot_predictions(tickers):
    # tickers = ["AAPL", "AMZN"]
    kpis = []

    ohlc_mon = {} # directory with ohlc value for each stock            
    start = dt.datetime.today()-dt.timedelta(3650)
    end = dt.datetime.today()

    # Loop over tickers and create a dataframe with close prices
    for ticker in tickers:
        ohlc_mon[ticker] = yf.download(ticker, start, end, interval='1mo')
        ohlc_mon[ticker].dropna(inplace=True, how="all")
    
    # Re-define tickers variable after removing any tickers with corrupted data
    tickers = ohlc_mon.keys()

    # Calculate monthly return for each stock and consolidate return info by stock in a separate dataframe
    ohlc_dict = copy.deepcopy(ohlc_mon)
    return_df = pd.DataFrame()
    for ticker in tickers:
        print("calculating monthly return for ", ticker)
        ohlc_dict[ticker]["mon_ret"] = ohlc_dict[ticker]["Adj Close"].pct_change()
        return_df[ticker] = ohlc_dict[ticker]["mon_ret"]
    return_df.dropna(inplace=True)

    # Calculating overall strategy's KPIs
    kpi_strategy = {}

    cagr_pflio = CAGR(pflio(return_df, len(tickers), len(tickers) // 2))
    print("CAGR: ", cagr_pflio)

    sharpe_pflio = sharpe(pflio(return_df, len(tickers), len(tickers) // 2), 0.025)
    print("Sharpe: ", sharpe_pflio)

    max_dd_pflio = max_dd(pflio(return_df, len(tickers), len(tickers) // 2))
    print("Max Drawdown: ", max_dd_pflio)

    kpi_strategy['CAGR'] = cagr_pflio
    kpi_strategy['sharpe'] = sharpe_pflio
    kpi_strategy['max_dd'] = max_dd_pflio

    kpis.append(kpi_strategy)

    # Calculating KPIs for Index buy and hold strategy over the same period
    DJI = yf.download("^DJI", dt.date.today()-dt.timedelta(3650), dt.date.today(), interval='1mo')
    DJI["mon_ret"] = DJI["Adj Close"].pct_change().fillna(0)

    DJI_return = DJI['mon_ret'].reset_index(drop=True)
    DJI_data = {
        "mon_ret": DJI_return
    }
    DJI_return_df = pd.DataFrame(DJI_data)
    

    kpi_index = {}

    cagr_index = CAGR(DJI)
    print("Index CAGR: ", cagr_index)

    sharpe_index = sharpe(DJI, 0.025)
    print("Index Sharpe: ", sharpe_index)

    max_dd_index = max_dd(DJI)
    print("Index Max Drawdown: ", max_dd_index)

    kpi_index['CAGR'] = cagr_index
    kpi_index['sharpe'] = sharpe_index
    kpi_index['max_dd'] = max_dd_index

    kpis.append(kpi_index)

    max_returns_strategy = (1+pflio(return_df, len(tickers), len(tickers) // 2)).cumprod()
    max_returns_index = (1+DJI_return_df).cumprod()

    return kpis, max_returns_strategy, max_returns_index


def get_json(stock_data_df):
    stock_data_dict = {}
    for col in stock_data_df.columns:
        stock_data_dict[col] = stock_data_df[[col]].reset_index().apply(lambda x: x[col], axis=1).tolist()

    return json.dumps(stock_data_dict)
