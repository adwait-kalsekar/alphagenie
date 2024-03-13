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
    context = {"page": page}
    return render(request, 'alphamarket/companies.html', context)

@login_required(login_url='login')
def errorPage(request, all_path):
    return render(request, 'alphamarket/error.html')