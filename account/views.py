from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .forms import RegisterForm
from account.models import Profile
from django.core.mail import send_mail
from command.utils import sendEmailToAdmin

# Create your views here.

@login_required
def account_page(request):
    return render(request, 'account/profile.html', {'page':'profile'})

def update_last_accessed_page(request):

    lastAccess = request.GET.get('lastAccessedPage', None)

    #Save the last page the user accessed
    try:
        #Get user profile
        userProfile = Profile.objects.get(user=request.user)

        #Set last accessed page with page passed in
        userProfile.lastPageAccessed = lastAccess
        userProfile.save()

        status = 'SUCCESS'
    except:
        status = 'FAILED'

    data = {
            'status': status
        }
    
    return JsonResponse(data)

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
                    lastName = form.cleaned_data['lastName'],
                    currentActiveLeague = None
                    )

                newProfile.save()

                #Send email to admin
                emailSubject = 'Onsidepick.com - New User Created'
                emailMessage = 'New user was created with username: ' + form.cleaned_data['username']
                sendEmailToAdmin(emailSubject, emailMessage)
        
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

def delete_account(request):
    #Delete user account
    try:
        request.user.delete()
        return redirect('/login/')
    except:
        print("Could not delete user.")
        return render(request, 'account/profile.html')

def login_redirect(request):
    if request.user.is_authenticated:
        #response = home(request)
        response = redirect('/home/')
    else:
        response = redirect('/login/')
    
    return response