from django.shortcuts import render

# Create your views here.

def index(request):
    page  = "home"
    context = {"page": page}
    return render(request, 'alphahome/index.html', context)

def about(request):
    page = "about"
    context = {"page": page}
    return render(request, 'alphahome/about.html', context)

def services(request):
    page = "services"
    context = {"page": page}
    return render(request, 'alphahome/services.html', context)