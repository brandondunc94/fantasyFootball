from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.core.mail import send_mail
from command.utils import sendEmailToAdmin
from .forms import RegisterForm
from account.models import Profile
from league.models import LeagueMembership, Team
from home.views import dashboard

# Create your views here.

@login_required
def account_page(request):
    leagueMemberships = LeagueMembership.objects.filter(user=request.user)
    userLeagues = [leagueMembership.league for leagueMembership in leagueMemberships]
    userProfile = Profile.objects.get(user=request.user)
    allTeams = Team.objects.all()

    return render(request, 'account/profile.html', 
    {
        'page':'profile',
        'leagueMemberships': leagueMemberships,
        'activeLeague': userProfile.currentActiveLeague,
        'userLeagues': userLeagues,
        'profile': userProfile,
        'teams': allTeams,
    })

@login_required
def public_account_page(request, username):
    if username:
        try:
            requestedUser = User.objects.get(username=username)
            leagueMemberships = LeagueMembership.objects.filter(user=requestedUser)
            userLeagues = [leagueMembership.league for leagueMembership in leagueMemberships]
            userProfile = Profile.objects.get(user=requestedUser)
            return render(request, 'account/publicProfile.html', 
            {
                'username': username,
                'leagueMemberships': leagueMemberships,
                'activeLeague': userProfile.currentActiveLeague,
                'userLeagues': userLeagues,
                'profile': userProfile,
            })
        except:
            #Could not retrieve user by username, default to the dashboard
            return dashboard(request)
    else:
        return dashboard(request)

#AJAX CALL
def update_profile(request):
    updatedFirstName = request.GET.get('firstName', None)
    updatedLastName = request.GET.get('lastName', None)
    updatedEmail = request.GET.get('email', None)
    updatedFavoriteTeam = request.GET.get('favoriteTeam', None)

    try:
        #Update user
        request.user.first_name = updatedFirstName
        request.user.last_name = updatedLastName
        request.user.email = updatedEmail

        #Updated user profile
        userProfile = Profile.objects.get(user=request.user)
        userProfile.firstName = updatedFirstName
        userProfile.lastName = updatedLastName
        if updatedFavoriteTeam:
            userProfile.favoriteTeam = Team.objects.get(name=updatedFavoriteTeam)

        request.user.save()
        userProfile.save()

        status = 'SUCCESS'
    except:
        status = 'FAILED'

    data = {
            'status': status
        }
    
    return JsonResponse(data)

#AJAX CALL
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