from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
import json
from league.utils import getUserLeagues, createNewSeason
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice
from account.models import Profile
#from home import classes

# Create your views here.
@login_required
def home(request):
    if request.method == "POST":
        #Get league from pick list or default to the first league found
        
        #Get week from pick list, otherwise default to week 1

        return render(request, 'home/home.html')
    elif request.method == "GET":
        
        #Do a lookup to find all leagues for current user
        userLeagues = getUserLeagues(request.user)

        if not userLeagues:
            return render(request, 'home/home.html')
        defaultLeague = userLeagues[0]
    
        #Set current active league for user
        currentProfile = Profile.objects.get(user=request.user)
        currentProfile.currentActiveLeague = defaultLeague
        currentProfile.save()

        leagueUsers = LeagueMembership.objects.filter(league=defaultLeague)

        if userLeagues == None:
            return render(request, 'home/home.html')
        else:
            #Initialize empty dictionary for gameData to be passed to template
            gameData = []

            #Determine week number to populate
            week = 1    #defaulting to 1 for now
            #weekData = Week.objects.get(id=1)
            currentWeekGames = Game.objects.filter(week_id=week)
            
            #We will eventually want to get the currentdate and compare it to the week start date and only grab that week
            for currentGame in currentWeekGames:
                #Check to see if there is pick data for this game
                currentGamePick = GameChoice.objects.filter(league=defaultLeague,user=request.user,week=week,game=currentGame)
                if currentGamePick:
                    currentPick = currentGamePick[0].winner
                else:
                    currentPick = ""
                gameData.append(
                {
                    'homeTeam' : getattr(currentGame, 'homeTeam'),
                    'homeScore' : getattr(currentGame, 'homeScore'),
                    'awayTeam' : getattr(currentGame, 'awayTeam'),
                    'awayScore' : getattr(currentGame, 'awayScore'),
                    'pick' : currentPick
                })
            return render(request, 'home/home.html', {'gameData': gameData, 'userLeagues': userLeagues, 'leagueUsers': leagueUsers})