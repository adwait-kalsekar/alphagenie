import yfinance as yf
import pandas as pd

ticker = "GOOGL"  # Example ticker symbol, replace it with your desired symbol
temp = yf.download(ticker, period='5y', interval='1d')

# Save the DataFrame to a CSV file
temp.to_csv('stock_data.csv')

print("Data saved to stock_data.csv successfully.")