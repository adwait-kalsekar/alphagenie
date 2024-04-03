from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def viewBots(request):
    page = "alphabots"
    context = {"page": page}
    return render(request, 'alphabots/viewBots.html', context)

@login_required(login_url='login')
def createBot(request):
    page = "alphabots"
    context = {"page": page}
    return render(request, 'alphabots/createBot.html', context)

@login_required(login_url='login')
def viewBuckets(request):
    page = "buckets"
    context = {"page": page}
    return render(request, 'alphabots/viewBuckets.html', context)

@login_required(login_url='login')
def createBucket(request):
    page = "buckets"
    context = {"page": page}
    return render(request, 'alphabots/createBucket.html', context)

@login_required(login_url='login')
def errorPage(request, all_path):
    return render(request, 'alphabots/error.html')