from django.shortcuts import render, redirect
from account.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import RegisterForm

# Create your views here.

@login_required
def account_page(request):
    return render(request, 'account/profile.html')

def create_account(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Trying to add " + form.cleaned_data['username'])
            #Check to see if username already exists
            existingUser = User.objects.filter(username=form.cleaned_data['username'])
            if existingUser:
                form = RegisterForm()
                return render(request, 'registration/register.html', {'form': form, 'error': "This username has already been taken. Please try a different one."})
            #Create new user using User model
            newUser = User.objects.create_user(
                username=form.cleaned_data['username'], 
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password']
                )

            #Login newUser
            if newUser is not None:
                login(request, newUser)
                #Create new profile using Profile model and pass in newUser
                newProfile = Profile(
                    user = newUser, 
                    firstName = form.cleaned_data['firstName'],
                    lastName = form.cleaned_data['lastName']
                    )
                    
                newProfile.save()
                return render(request, 'home/welcome.html')
        else:
            form = RegisterForm()
            return render(request, 'registration/register.html', {'form': form, 'error': "Please fill out all required fields."})
    elif request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'account/profile.html')
        else:
            form = RegisterForm()
            return render(request, 'registration/register.html', {'form': form})

