from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.db import models
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import json
import pandas as pd
from .models import StockSymbol, Bucket, TradingBot, Strategy, Backtesting
from .utils.data_downloader import fetch_adj_close_data, fetch_data
from .utils.kpi import CAGR, volatility, sharpe, sortino, max_dd, calmar
from .utils.bot_script import get_bot_predictions, get_json

# Create your views here.

@login_required(login_url='login')
def viewBots(request):
    page = "alphabots"

    # get all trading bots for this user
    try:
        user = request.user
        bots = TradingBot.objects.filter(user=user.traderprofile)

        current_value_sum = bots.aggregate(current_value_sum=models.Sum('current_value'))['current_value_sum']
        current_value_sum = current_value_sum or 0

        user.traderprofile.total_returns = current_value_sum
        user.traderprofile.save()

    except Exception as e:
        print(e)
        return errorPage(request, "500", "Error Fetching bots", "There was an error Fetching Trading Bots. Please Try Again")

    context = {"page": page, "bots": bots, "total_bots": len(bots)}
    return render(request, 'alphabots/viewBots.html', context)

@login_required(login_url='login')
def createBot(request):
    page = "alphabots"

    user = request.user
    strategies = Strategy.objects.all()
    backtesting = Backtesting.objects.all()

    if request.method == 'POST':
        try:
            bot_name = request.POST.get('bot_name')
            bucket_id = request.POST.get('bucket_id')
            bucket = Bucket.objects.get(id=bucket_id)
            strategy_id = request.POST.get('strategy_id')
            strategy = Strategy.objects.get(id=strategy_id)
            investment_amount = int(request.POST.get('investment_amount'))

            if investment_amount > request.user.traderprofile.funds:
                return errorPage(request, "500", "Error Creating αlphaBot", "There was an error Creating the αlphaBot. You do not have enough funds in your wallet to invest this amount. Please Try Again")

            new_bot = TradingBot.objects.create(name=bot_name, user=request.user.traderprofile, bucket=bucket, strategy=strategy, amount_invested=investment_amount)

            print(new_bot)

            new_bot.save()
            request.user.traderprofile.funds -= investment_amount
            request.user.traderprofile.total_invested += investment_amount
            request.user.traderprofile.save()

            return redirect("viewBots")
        
        except Exception as e:
            print(e)
            return errorPage(request, "500", "Error Creating αlphaBot", "There was an error Creating the αlphaBot. Please Try Again")
        
    buckets = Bucket.objects.filter(user=user.traderprofile)
    context = {"page": page, "buckets": buckets, "strategies": strategies, "backtesting": backtesting}
    return render(request, 'alphabots/createBot.html', context)

@login_required(login_url='login')
def change_bot_status(request, id):
    try:
        bot_id = int(id)
        bot = TradingBot.objects.get(id=bot_id)
        if bot.is_deployed == True:
            bot.is_deployed = False
        else:
            bot.is_deployed = True
        bot.save()
        return redirect("viewBots")
    
    except Exception as e:
        print(e)
        return errorPage(request, "500", "Error Changing status", "There was an error Changing the Active status of your αlphaBot. Please Try Again")
    
@login_required(login_url='login')
def botDetails(request, id):
    page = "alphabots"

    trader = request.user
    try:
        bot_id = int(id)
        bot = TradingBot.objects.get(Q(id=bot_id) & Q(user=trader.traderprofile))
        bucket = bot.bucket
        bucket_stocks = bucket.symbols.all()
        tickers = []
        for stock in bucket_stocks:
            tickers.append(stock.symbol)

        kpis, max_returns_strategy, max_returns_index = get_bot_predictions(tickers)

        max_returns_strategy_json = get_json(max_returns_strategy)
        max_returns_index_json = get_json(max_returns_index)

        total_sum = max_returns_strategy['mon_ret'].sum()
        bot.current_value = total_sum
        bot.save()

        print("Total sum of mon_ret:", total_sum)
        
        context = {"page": page, "bucket": bucket, "tickers": tickers, "strategy_kpi": kpis[0], "index_kpi": kpis[1], "max_return_strategy_json": max_returns_strategy_json, "max_return_index_json": max_returns_index_json}
        return render(request, "alphabots/botDetails.html", context)
    except Exception as e:
        print(e)
        return errorPage(request, "404", "Error Fetching bucket", "There was an error Fetching the Stock bucket. Please Try Again")
        
@login_required(login_url='login')
def generate_script(request, bot_id):
    script_data = request.POST.get('script_data', '')
    script_content = f"# Generated Python Script\nprint({repr(script_data)})\n"
    response = HttpResponse(script_content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="generated_script.py"'
    return response

@login_required(login_url='login')
def viewBuckets(request):
    page = "buckets"

    try:
        user = request.user
        buckets = Bucket.objects.filter(user=user.traderprofile)
    except Exception as e:
        print(e)
        return errorPage(request, "500", "Error Fetching buckets", "There was an error Fetching Stock buckets. Please Try Again")
    
    context = {"page": page, "buckets": buckets, 'total_buckets': len(buckets)}
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
def deleteBot(request, id):
    page = "bots"

    context = {"page": page, "delete_message": "Confirm Delete Bot?", "resource": "bot", "id": id}
    return render(request, 'alphabots/confirmDelete.html', context)

@login_required(login_url='login')
def confirmDelete(request, resource, id):
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
    
    elif resource == "bot":
        try:
            bot_id = int(id)
            user = request.user
            bot = TradingBot.objects.get(Q(id=bot_id) & Q(user=user.traderprofile))
            bot.delete()

            return redirect("viewBots")
    
        except Exception as e:
            print(e)
            return errorPage(request, "500", "Error Deleting αlphaBot", "There was an error Deleting the αlphaBot. Please Try Again")
        
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

        print(stock_data_json)

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