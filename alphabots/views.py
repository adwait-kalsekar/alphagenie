from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
import pandas as pd
from .models import StockSymbol, Bucket, TradingBot, Strategy, Backtesting
from .utils.data_downloader import fetch_adj_close_data, fetch_data
from .utils.kpi import CAGR, volatility, sharpe, sortino, max_dd, calmar

# Create your views here.

@login_required(login_url='login')
def viewBots(request):
    page = "alphabots"

    # get all trading bots for this user
    try:
        user = request.user
        bots = TradingBot.objects.filter(user=user.traderprofile)
    except Exception as e:
        print(e)
        return errorPage(request, "500", "Error Fetching bots", "There was an error Fetching Trading Bots. Please Try Again")

    context = {"page": page, "bots": bots}
    return render(request, 'alphabots/viewBots.html', context)

@login_required(login_url='login')
def createBot(request):
    page = "alphabots"
    
    user = request.user

    strategies = Strategy.objects.all()
    backtesting = Backtesting.objects.all()
    buckets = Bucket.objects.filter(user=user.traderprofile)
    context = {"page": page, "buckets": buckets, "strategies": strategies, "backtesting": backtesting}
    return render(request, 'alphabots/createBot.html', context)

@login_required(login_url='login')
def viewBuckets(request):
    page = "buckets"

    try:
        user = request.user
        buckets = Bucket.objects.filter(user=user.traderprofile)
    except Exception as e:
        print(e)
        return errorPage(request, "500", "Error Fetching buckets", "There was an error Fetching Stock buckets. Please Try Again")
    
    context = {"page": page, "buckets": buckets}
    return render(request, 'alphabots/viewBuckets.html', context)

@login_required(login_url='login')
def createBucket(request):
    page = "buckets"

    if request.method == 'POST':
        try:
            bucket_name = request.POST.get('bucket_name')
            symbol_list = request.POST.getlist('symbol_list')

            new_bucket = Bucket.objects.create(name=bucket_name, user=request.user.traderprofile)
            for symbol_id in symbol_list:
                symbol = StockSymbol.objects.get(id=symbol_id)
                new_bucket.symbols.add(symbol)

            new_bucket.save()

            return redirect("viewBuckets")
        
        except Exception as e:
            print(e)
            if new_bucket:
                new_bucket.delete()
            return errorPage(request, "500", "Error Creating Bucket", "There was an error Creating the Stock bucket. Please Try Again")

    stock_symbols = StockSymbol.objects.all()
    context = {"page": page, "stock_symbols": stock_symbols}
    return render(request, 'alphabots/createBucket.html', context)

@login_required(login_url='login')
def deleteBucket(request, id):
    page = "buckets"

    context = {"page": page, "delete_message": "Confirm Delete Bucket?", "resource": "bucket", "id": id}
    return render(request, 'alphabots/confirmDelete.html', context)

@login_required(login_url='login')
def confirmDeleteBucket(request, resource, id):
    if resource == "bucket":
        try:
            bucket_id = int(id)
            user = request.user
            bucket = Bucket.objects.get(Q(id=bucket_id) & Q(user=user.traderprofile))
            bucket.delete()

            return redirect("viewBuckets")
    
        except Exception as e:
            print(e)
            return errorPage(request, "500", "Error Deleting Bucket", "There was an error Deleting the Stock bucket. Please Try Again")
    
    else:
        return errorPage(request, "404", "Resource Not Found", "The Resource you mentioned is incorrect.")

@login_required(login_url='login')
def bucketDetails(request, id):
    page = "buckets"
    trader = request.user
    try:
        bucket_id = int(id)
        bucket = Bucket.objects.get(Q(id=bucket_id) & Q(user=trader.traderprofile))
        bucket_stocks = bucket.symbols.all()
        tickers = []
        for stock in bucket_stocks:
            tickers.append(stock.symbol)

        period = request.GET.get("period")
        if period == None:
            period = '1mo'

        stock_data_df = fetch_adj_close_data(tickers, period)

        # Replace NaN values with None
        stock_data_df = stock_data_df.dropna()

        # Convert the DataFrame to a dictionary
        stock_data_dict = {}
        for col in stock_data_df.columns:
            stock_data_dict[col] = stock_data_df[[col]].reset_index().apply(lambda x: [x['Date'].strftime('%Y-%m-%d'), x[col]], axis=1).tolist()

        # Convert the dictionary to JSON format
        stock_data_json = json.dumps(stock_data_dict)

        stock_kpi = {}
        for ticker in tickers:
            df = fetch_data(ticker, period)
            stock_kpi[ticker] = {}
            stock_kpi[ticker]["CAGR"] = CAGR(df)
            stock_kpi[ticker]["Volatility"] = volatility(df)
            stock_kpi[ticker]["Sharpe"] = sharpe(df)
            stock_kpi[ticker]["Sortino"] = sortino(df)
            stock_kpi[ticker]["Max_Drawdown"] = max_dd(df)
            stock_kpi[ticker]["Calmar_Ratio"] = calmar(df)

        print(stock_kpi)
        
        context = {"page": page, "bucket": bucket, "tickers": tickers, "stock_data_json": stock_data_json, "period": period, "stock_kpi": stock_kpi}
        return render(request, "alphabots/bucketDetails.html", context)
    except Exception as e:
        print(e)
        return errorPage(request, "404", "Error Fetching bucket", "There was an error Fetching the Stock bucket. Please Try Again")
    

@login_required(login_url='login')
def pageNotFoundError(request, all_path):
    return errorPage(request, 404, "Page not found", "We’re sorry, the page you have looked for does not exist in our website!") 

def errorPage(request, error_code, error_message, error_info):
    context = {"error_code": error_code, "error_message": error_message, "error_info": error_info}
    return render(request, 'alphabots/error.html', context)