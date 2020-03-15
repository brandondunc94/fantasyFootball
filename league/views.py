from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from league.forms import NewLeagueForm
from league.utils import getUserLeagues
from league.models import League, LeagueMembership, LeagueMessage
from account.models import Profile

# Create your views here.
@login_required
def home(request, leagueName=""):
    
    if request.method == "GET":
        #Do a lookup to find all leagues for current user. If none, default to home page with no data
        userLeagues = getUserLeagues(request.user)
        if not userLeagues:
            return render(request, 'home/home.html')

        #Get user profile
        currentProfile = Profile.objects.get(user=request.user)

        #Get current active league and set it in user profile
        if leagueName:
            #Get league passed into view
            activeLeague = League.objects.filter(name=leagueName)
            if not activeLeague:
                #No league found using name passed in, default to first league found
                activeLeague = userLeagues[0]
            else:
                #League found, there can only be 1 so grab first found league from query set
                activeLeague = activeLeague[0]                 
            currentProfile.currentActiveLeague = activeLeague
            currentProfile.save()
        else:
            #Default to last used league
            activeLeague = currentProfile.currentActiveLeague

        #Get all users for active league
        leagueUsers = LeagueMembership.objects.filter(league=activeLeague).order_by('-score')

        #Get all messages for current league to populate message board
        leagueMessages = LeagueMessage.objects.filter(league=activeLeague)

        return render(request, 'league/leagueHome.html', {'userLeagues': userLeagues, 'leagueUsers': leagueUsers, 'activeLeague': activeLeague.name, 'leagueMessages': leagueMessages})
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
            newLeague = League.objects.create(name=form.cleaned_data['name'])

            #Assign current user to new league - FIX THIS
            leagueMembership = LeagueMembership.objects.create(user=request.user,league=newLeague)
            
            #Get user profile and set newLeague to active league
            currentProfile = Profile.objects.get(user=request.user)
            currentProfile.currentActiveLeague = newLeague
            currentProfile.save()

            #Return to home page
            return redirect('home')
            
    elif request.method == "GET":
            form = NewLeagueForm()
            return render(request, 'league/createLeague.html', {'form': form})

def joinLeague(request):
    if request.method == "POST":
        #Get league name from POST request
        leagueName = request.POST.get("league", "")

        #Get league object from DB
        league = League.objects.get(name=leagueName)
        
        #Join current user to the league
        leagueMembership = LeagueMembership.objects.create(user=request.user,league=league)

        #Get user profile and set newly jioned league to active league
        currentProfile = Profile.objects.get(user=request.user)
        currentProfile.currentActiveLeague = league
        currentProfile.save()

        return redirect('home')
    if request.method == "GET":
        #Query for leagues and render on page
        leagues = League.objects.all()
        return render(request, 'league/joinLeague.html', {'leagues': leagues})
