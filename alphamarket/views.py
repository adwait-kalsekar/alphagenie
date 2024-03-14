from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def index(request):
    page = "dashboard"
    context = {"page": page}
    return render(request, 'alphamarket/dashboard.html', context)

@login_required(login_url='login')
def markets(request):
    page = "markets"
    tickers = ["NVDA", "MSFT", "AAPL", "AMZN", "UNH", "BRK.B", "META", "LLY", "ORCL", "IBM"]
    tickers_with_index = zip(range(len(tickers)), tickers)
    context = {"page": page, "tickers": tickers_with_index}
    return render(request, 'alphamarket/markets.html', context)

@login_required(login_url='login')
def market_details(request, ticker):
    page = "markets"
    
    context = {"page": page, "ticker": ticker}
    return render(request, 'alphamarket/market_details.html', context)

@login_required(login_url='login')
def errorPage(request, all_path):
    return render(request, 'alphamarket/error.html')