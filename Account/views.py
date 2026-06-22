from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm,LoginForm
from django.core.mail import send_mail
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='login/')
def home(request):
    return render(request, 'home.html')









def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')  
    else:
        form = RegistrationForm()
        
    return render(request, 'signup.html', {'form': form})








def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user) 
                return redirect('home')  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})





def logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'login.html') 

