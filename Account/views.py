from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.core.mail import send_mail



def home(request):
    return render(request, 'home.html')






# def login(request):
#     return render(request, 'login.html')







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




send_mail(
    'Welcome to My Site!',
    'Thanks for signing up. Glad to have you!',
    'deepti@thoughtwin.com',        
    ['deeptibindia708.com'],        
    fail_silently=False,
)




from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import RegistrationForm

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
         
            user = form.save()  
            username = form.cleaned_data.get('username')
            user_email = form.cleaned_data.get('email') 
        
            send_mail(
                subject='Welcome to My Site!',
                message='Thanks for signing up. Glad to have you!',
                from_email='deepti@thoughtwin.com',        
                recipient_list=[user_email],        
                fail_silently=False,
            )
            
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')  
    else:
        form = RegistrationForm()
        
    return render(request, 'signup.html', {'form': form})
