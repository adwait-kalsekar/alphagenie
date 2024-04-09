from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def loginUser(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'alphatrader/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'alphatrader/login.html')

def signupUser(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        if password != password2:
            return render(request, 'alphatrader/signup.html', {'error': 'Passwords do not match'})
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name') or ' '
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'alphatrader/signup.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect(reverse('homepage'))

@login_required(login_url='login')
def profile(request):
    page = "profile"
    context = {"page": page}
    return render(request, 'alphatrader/profile.html', context)

@login_required(login_url='login')
def updateProfile(request):
    if request.method == 'POST':
        # Assuming you have a form to update the profile data
        user = request.user
        traderProfile = user.traderprofile

        if 'profile_image' in request.FILES:
            print("hello")
            profile_image = request.FILES['profile_image']
            request.user.traderprofile.profile_image = profile_image
            request.user.traderprofile.save()

        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        if f_name:
            user.first_name = f_name
        if l_name:
            user.last_name = l_name
        if username:
            user.username = username
        if email:
            user.email = email
        
        user.save()

        print(user, traderProfile)
    return redirect(reverse('profile'))

@login_required(login_url='login')
def updatePassword(request):
    print('Updating password')
    return redirect(reverse('profile'))

@login_required(login_url='login')
def wallet(request):
    page = "wallet"

    if request.method == 'POST':
        try:
            user = request.user
            traderProfile = user.traderprofile
            amount = int(request.POST.get('amount'))
            if amount > 100000:
                raise Exception('Amount too high')
            if amount:
                traderProfile.funds = traderProfile.funds + amount
                traderProfile.save()
        except Exception as e:
            print(e)
            return errorPage(request, "500", "Error Adding Funds", "There was an error adding funds to your wallet. Check the Amount and Try Again.")

    context = {"page": page}
    return render(request, 'alphatrader/wallet.html', context)

@login_required(login_url='login')
def pageNotFoundError(request, all_path):
    return errorPage(request, 404, "Page not found", "We’re sorry, the page you have looked for does not exist in our website!") 

def errorPage(request, error_code, error_message, error_info):
    context = {"error_code": error_code, "error_message": error_message, "error_info": error_info}
    return render(request, 'alphabots/error.html', context)