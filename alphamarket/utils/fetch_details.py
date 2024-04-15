import yfinance as yf
import pandas as pd
from django.conf import settings
from alphabots.models import StockSymbol
import os
import json

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

def convert_to_integer(duration_str):
    # Remove leading and trailing whitespace
    duration_str = duration_str.strip()
    
    # Check if the last character is 'y' or 'mo' and extract accordingly
    if duration_str.endswith('y'):
        # Extract the numeric part of the string
        numeric_part = duration_str[:-1]
        duration_int = int(numeric_part)
        return int(duration_int) * 365
    elif duration_str.endswith('mo'):
        numeric_part = duration_str[:-2]
        duration_int = int(numeric_part)
        return int(duration_int) * 30
    else:
        raise ValueError("Invalid duration format: '{}'".format(duration_str))
    

def get_json(stock_data_df):
    stock_data_dict = {}
    for col in stock_data_df.columns:
        stock_data_dict[col] = stock_data_df[[col]].reset_index().apply(lambda x: [x['Date'].strftime('%Y-%m-%d'), x[col]], axis=1).tolist()

    return json.dumps(stock_data_dict)