from django.shortcuts import render
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
            print(form.cleaned_data['username'])
            #Create new user using User model
            newUser = User.objects.create_user(form.cleaned_data['username'], 'bro_duncan18@yahoo.com'
                                                ,form.cleaned_data['password'])
            #Login newUser
            if newUser is not None:
                login(request, newUser)
                #Create new profile using Profile model and pass in newUser
                newProfile = Profile(user = newUser, bio = "I like football.", location = "Seattle")
                newProfile.save()
                return render(request, 'home/home.html')
    elif request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'account/profile.html')
        else:
            form = RegisterForm()
            return render(request, 'registration/register.html', {'form': form})
