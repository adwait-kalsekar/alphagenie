from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from alphabots.models import StockSymbol
from alphamarket.utils.fetch_details import fetch_data, get_json
from alphamarket.utils.stock_data_types import StockDataTypes

# Create your views here.

@login_required(login_url='login')
def index(request):
    page = "dashboard"
    context = {"page": page}
    return render(request, 'alphamarket/dashboard.html', context)

@login_required(login_url='login')
def markets(request):
    page = "markets"
    tickers = StockSymbol.objects.all()
    tickers_with_index = zip(range(len(tickers)), tickers)
    context = {"page": page, "tickers": tickers_with_index}
    return render(request, 'alphamarket/markets.html', context)

@login_required(login_url='login')
def marketDetails(request, ticker):
    page = "markets"

    try:
        period = request.GET.get("period")
        if period == None:
            period = '1mo'

        stock_data_adj_close = fetch_data(ticker, period, StockDataTypes.ADJ_CLOSE.value)
        stock_data_open = fetch_data(ticker, period, StockDataTypes.OPEN.value)
        stock_data_close = fetch_data(ticker, period, StockDataTypes.CLOSE.value)
        stock_data_high = fetch_data(ticker, period, StockDataTypes.HIGH.value)
        stock_data_low = fetch_data(ticker, period, StockDataTypes.LOW.value)
        stock_data_volume = fetch_data(ticker, period, StockDataTypes.VOLUME.value)

        stock_data_adj_close = get_json(stock_data_adj_close)
        stock_data_open = get_json(stock_data_open)
        stock_data_close = get_json(stock_data_close)
        stock_data_high = get_json(stock_data_high)
        stock_data_low = get_json(stock_data_low)
        stock_data_volume = get_json(stock_data_volume)
        
        context = {
            "page": page, 
            "ticker": ticker, 
            "stock_data_adj_close": stock_data_adj_close, 
            "stock_data_open": stock_data_open, 
            "stock_data_close": stock_data_close, 
            "stock_data_high": stock_data_high, 
            "stock_data_low": stock_data_low, 
            "stock_data_volume": stock_data_volume,
            "period": period
        }
        return render(request, 'alphamarket/marketDetails.html', context)
    
    except Exception as e:
        print(e)
        return errorPage(request, "404", "Error Fetching Details", "There was an error Fetching the Stock Market Details. Please Try Again")


@login_required(login_url='login')
def errorPage(request, all_path):
    return render(request, 'alphamarket/error.html')