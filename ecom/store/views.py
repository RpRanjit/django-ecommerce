from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from .forms import SignUpForm


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            messages.success(request, "Username or Password you entered is incorrect. Pleasr try again.")
            return redirect('login')
            
    return render(request, 'login.html', {})

def logout_view(request):
      logout(request)
      messages.success(request, "You have been sucessfully Logout.")
      return redirect('home')

def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username= username,password = password )
            login(request, user)
            messages.success(request,'You are registered to Newa Ecommerce.')
            return redirect('home')
        else:
            messages.success(request,'Oops! Something is wrong. Please register again.')
            return redirect('register')
    else:
        return render(request, 'register.html',{'form': form})