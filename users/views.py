import re
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html')

def login_request(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #Save off username and password
            inputUsername = form.cleaned_data.get("username")
            inputPassword = form.cleaned_data.get("password")

            #Query for username and password combination
            #user = User.objects.filter(email = inputEmail, password = inputPassword)
            user = authenticate(username=inputUsername, password = inputPassword)
            if user is not None:
                # If user exists, redirect to homepage:
                login(request, user)
                return render(request, 'home.html')
            else:
                print("Invalid user credentials.")
                return render(request, "users/login.html")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def create_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #Save off username and password
            inputUsername = form.cleaned_data.get("username")
            inputPassword = form.cleaned_data.get("password")

            #Query for username and password combination
            #user = User.objects.filter(email = inputEmail, password = inputPassword)
            user = authenticate(username=inputUsername, password = inputPassword)
            if user is not None:
                # If user exists, redirect to homepage:
                login(request, user)
                return render(request, 'home.html')
            else:
                print("Invalid user credentials.")
                return render(request, "users/login.html")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignUpForm()
    
    return render(request, 'users/newUser.html', {'form': form})