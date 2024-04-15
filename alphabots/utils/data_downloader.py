import yfinance as yf
import pandas as pd
from django.conf import settings
from alphabots.models import StockSymbol
import os

def download_data(tickers=[], period='10y'):
    cl_price = pd.DataFrame()
    static_dir = settings.STATICFILES_DIRS[0] 

    datasets_dir = os.path.join(static_dir, 'datasets')

    if not os.path.exists(datasets_dir):
        os.makedirs(datasets_dir)

    if len(tickers) == 0:
        stock_symbol = StockSymbol.objects.all()
        for stock in stock_symbol:
            tickers.append(stock.symbol)

    for ticker in tickers:
        try:
            cl_price[ticker] = yf.download(ticker, period=period)["Adj Close"]
            data = yf.download(ticker, period='10y')
            df = data.reset_index()

            file_path = os.path.join(datasets_dir, f'{ticker}.csv')

            df.to_csv(file_path, index=False)
        except Exception as e:
            print(f"Failed to download data for {ticker}: {e}")

    file_path = os.path.join(datasets_dir, 'combined_adj_close.csv')
    cl_price.to_csv(file_path, index='Date')

def fetch_data(ticker, period='10y', type='Adj Close'):
    static_dir = settings.STATICFILES_DIRS[0]  
    datasets_dir = os.path.join(static_dir, 'datasets')
    file_path = os.path.join(datasets_dir, f'{ticker}.csv')

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError("CSV file not found.")

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    print(df.columns)

    print(df)

    df['Date'] = pd.to_datetime(df['Date'])

    # Set the 'Date' column as the index
    df.set_index('Date', inplace=True)

    # Create a new DataFrame to store filtered data
    filtered_df = pd.DataFrame()
    
    filtered_df[type] = df[type]
    
    start_date = pd.Timestamp.now() - pd.Timedelta(days=convert_to_integer(period))

    filtered_df = filtered_df[filtered_df.index >= start_date]
    filtered_df = filtered_df.dropna()

    return filtered_df

def fetch_adj_close_data(tickers, period='10y'):
    static_dir = settings.STATICFILES_DIRS[0]
    datasets_dir = os.path.join(static_dir, 'datasets')
    file_path = os.path.join(datasets_dir, 'combined_adj_close.csv')

    if not os.path.exists(file_path):
        raise FileNotFoundError("CSV file not found.")

    df = pd.read_csv(file_path)

    print(df.columns)

    print(df)

    df['Date'] = pd.to_datetime(df['Date'])

    df.set_index('Date', inplace=True)

    filtered_df = pd.DataFrame()

    for ticker in tickers:
        if ticker in df.columns:
            filtered_df[ticker] = df[ticker]
    
    start_date = pd.Timestamp.now() - pd.Timedelta(days=convert_to_integer(period))

    filtered_df = filtered_df[filtered_df.index >= start_date]
    print(filtered_df)

    return filtered_df

def convert_to_integer(duration_str):
    duration_str = duration_str.strip()
    
    if duration_str.endswith('y'):
        numeric_part = duration_str[:-1]
        duration_int = int(numeric_part)
        return int(duration_int) * 365
    elif duration_str.endswith('mo'):
        numeric_part = duration_str[:-2]
        duration_int = int(numeric_part)
        return int(duration_int) * 30
    else:
        raise ValueError("Invalid duration format: '{}'".format(duration_str))

    