from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm

def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('register') 
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login')
        else:
            pass
    return render(request, 'account/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  
