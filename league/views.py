from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from league.forms import NewLeagueForm
from league import utils as leagueUtils
from league.models import League, LeagueMembership, LeagueMessage, LeagueMembershipRequest
from account.models import Profile

# Create your views here.
@login_required
def home(request, leagueName=""):
    
    if request.method == "GET":
        #Do a lookup to find all leagues for current user. If none, default to home page with no data
        userLeagues = leagueUtils.getUserLeagues(request.user)
        if userLeagues == None:
            return render(request, 'home/welcome.html')

        #Get user profile
        currentProfile = Profile.objects.get(user=request.user)

        #Get league passed into view
        activeLeague = leagueUtils.getLeague(leagueName)
        if activeLeague == None:
            #No league found using name passed in, default to user's current active league
            activeLeague = leagueUtils.getUserActiveLeague(request.user)
        else:
            #Set current league to user's active league in Profile
            leagueUtils.setUserActiveLeague(request.user, activeLeague)

        #Check if current user is an admin of the league - this will display the 'League Settings' button if true
        try:
            League.objects.get(admin=request.user)
            leagueAdmin = True
        except:
            leagueAdmin = False

        #Get all users for active league
        leagueUsers = LeagueMembership.objects.filter(league=activeLeague).order_by('-score')

        #Get all messages for current league to populate message board
        leagueMessages = LeagueMessage.objects.filter(league=activeLeague)

        return render(request, 'league/leagueHome.html', {'userLeagues': userLeagues, 'leagueUsers': leagueUsers, 'activeLeague': activeLeague.name, 'leagueMessages': leagueMessages, 'leagueAdmin': leagueAdmin})
    elif request.method == "POST":
        #Log message
        newMessage = request.POST.get("message", "")

        if not newMessage:
            return render(request, 'league/leagueHome.html')
        else:
            #Get active league
            userProfile = Profile.objects.get(user=request.user)
            activeLeague = userProfile.currentActiveLeague

            newLeagueMessage = LeagueMessage.objects.create(user=request.user, league=activeLeague, message=newMessage)
            newLeagueMessage.save()

        return redirect("/league/home/")
    else:
         return render(request, 'league/leagueHome.html')

def leagueAdmin(request, leagueName=""):
    
    if leagueName:
        try:
            #Check to see if current user is an admin
            activeLeague = League.objects.get(name=leagueName, admin=request.user)
        except:
            #User is not an admin or the league does not exist
            return redirect("/home/")
    else:
        #League name not passed in, redirect to home page
        return redirect("/home/")

    #Get league users
    leagueUsers = LeagueMembership.objects.filter(league=activeLeague)

    #Get leagueRequests
    leagueRequests = LeagueMembershipRequest.objects.filter(league=activeLeague)
    return render(request, 'league/leagueAdmin.html', {'leagueUsers': leagueUsers, 'leagueRequests': leagueRequests, 'activeLeague': activeLeague})

def createLeague(request):
    if request.method == "POST":
        form = NewLeagueForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['name'])
            #Check to see if this league name already exists
            existingLeague = League.objects.filter(name=form.cleaned_data['name'])
            if existingLeague:
                form = NewLeagueForm()
                return render(request, 'league/createLeague.html', {'form': form, 'error': 'The League name you entered has already been taken. Please try another League name.'})
            
            #Create new league model in db
            newLeague = League.objects.create(name=form.cleaned_data['name'], admin=request.user, description=form.cleaned_data['description'])

            #Assign current user to new league
            leagueMembership = LeagueMembership.objects.create(user=request.user,league=newLeague)
            
            #Set newLeague to active league for current user - THIS IS VERY IMPORTANT
            leagueUtils.setUserActiveLeague(request.user, newLeague)

            #Return to home page
            return redirect('home')
            
    elif request.method == "GET":
            form = NewLeagueForm()
            return render(request, 'league/createLeague.html', {'form': form})

def joinLeaguePage(request):
    #Query for leagues and render on page
    leagues = League.objects.exclude(members__username__iexact=request.user.username)
    leagueData = []
    for currentLeague in leagues:
        #Query to see if the user has already requested to join the current league
        pendingRequest = LeagueMembershipRequest.objects.filter(user=request.user, league=currentLeague)
        if pendingRequest:
            leagueData.append(
            {
                'pendingRequest': True,
                'league': currentLeague
            })
        else:
            leagueData.append(
            {
                'pendingRequest': False,
                'league': currentLeague
            })
    return render(request, 'league/joinLeague.html', {'leagueData': leagueData})

def requestLeague(request, leagueName=""):

    #Get league name from POST request
    if not leagueName:
        redirect('/league/join/')

    #Get league object from DB
    try:
        activeLeague = League.objects.get(name=leagueName)
    except:
        print("League not found when searchd: " + leagueName)

    #Make sure the user is not already part of this league
    try:
        leagueMember = LeagueMembership.objects.get(user=request.user,league=activeLeague)
        if leagueMember:
            #User is already a member, redirect them home
            return redirect('/league/join/')
    except:
        #Create request to join the league
        membershipRequest = LeagueMembershipRequest.objects.create(user=request.user,league=activeLeague)

    return redirect('/league/join/')


def addToLeague(request, username="", leagueName=""):
    if not username:
        return redirect('/league/home/')
    if not leagueName:
        return redirect('/league/home/')
    #Make sure current user is the admin of the league
    try:
        leagueAdmin = League.objects.get(admin=request.user)
    except:
        return redirect('/league/home/')

    #Get user from username
    requestedUser = User.objects.get(username=username)
    #Create new league membership object
    newMembership = LeagueMembership.objects.create(league=leagueAdmin, user=requestedUser)

    #Set newly joined league to active league for requested user
    leagueUtils.setUserActiveLeague(requestedUser, leagueAdmin)

    #Delete request to join league
    try:
        leagueRequest = LeagueMembershipRequest.objects.get(user=requestedUser, league=leagueAdmin)
        leagueRequest.delete()
    except:
        print("Error - could not delete league membership request.")

    return render(request, 'league/joinLeague.html')
