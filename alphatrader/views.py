from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

# Create your views here.

def index(request):
    return render(request, 'alphatrader/dashboard.html')

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'alphatrader/dashboard.html')
        else:
            return render(request, 'alphatrader/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'alphatrader/login.html')
    
def logoutUser(request):
    logout(request)
    return render(request, 'alphatrader/login.html')

def signupUser(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # email = request.POST.get('email')
        # user = User.objects.create_user(username=username, password=password, email=email)
        # user.save()
        return render(request, 'alphatrader/signup.html')
    else:
        return render(request, 'alphatrader/signup.html')