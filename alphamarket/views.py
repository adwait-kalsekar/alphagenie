from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from alphabots.models import StockSymbol
from alphamarket.utils.fetch_details import fetch_data, get_json, fetch_data_for_pred
from alphamarket.utils.predict import predict_data
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
def predictions(request):
    page = "predictions"
    tickers = StockSymbol.objects.all()
    tickers_with_index = zip(range(len(tickers)), tickers)
    context = {"page": page, "tickers": tickers_with_index}
    return render(request, 'alphamarket/predictions.html', context)

@login_required(login_url='login')
def predictionDetails(request, ticker):
    page = "predictions"

    try:
        stock_data_adj_close = fetch_data_for_pred(ticker, StockDataTypes.ADJ_CLOSE.value)
        
        predicted_data = predict_data(ticker, stock_data_adj_close)
        print(predicted_data)

        stock_data_adj_close = get_json(stock_data_adj_close)

        predicted_data  = get_json(predicted_data)
        
        context = {
            "page": page, 
            "ticker": ticker, 
            "stock_data_adj_close": stock_data_adj_close,
            "predicted_data": predicted_data,
        }
        return render(request, 'alphamarket/predictionDetails.html', context)
    
    except Exception as e:
        print(e)
        return errorPage(request, "404", "Error Fetching Details", "There was an error Fetching the Stock Market Details. Please Try Again")


@login_required(login_url='login')
def pageNotFoundError(request, all_path):
    return errorPage(request, 404, "Page not found", "We’re sorry, the page you have looked for does not exist in our website!") 

def errorPage(request, error_code, error_message, error_info):
    context = {"error_code": error_code, "error_message": error_message, "error_info": error_info}
    return render(request, 'alphabots/error.html', context)