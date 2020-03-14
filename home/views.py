from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
import json
from league.utils import getUserLeagues
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice
from account.models import Profile
#from home import classes

# Create your views here.
@login_required
def home(request, weekId="1", leagueName=""):
        
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
    
    #Get game data for weekId passed in
    currentWeekGames = Game.objects.filter(week_id=weekId)
    
    #Initialize empty dictionary for gameData to be passed to template
    gameData = []

    #We will eventually want to get the currentdate and compare it to the week start date and only grab that week
    for currentGame in currentWeekGames:
        #Check to see if there is pick data for this game
        currentGamePick = GameChoice.objects.filter(league=activeLeague,user=request.user,week=weekId,game=currentGame)
        if currentGamePick:
            currentPick = currentGamePick[0].winner
        else:
            currentPick = "None"
        gameData.append(
        {
            'homeTeam' : getattr(currentGame, 'homeTeam'),
            'homeScore' : getattr(currentGame, 'homeScore'),
            'awayTeam' : getattr(currentGame, 'awayTeam'),
            'awayScore' : getattr(currentGame, 'awayScore'),
            'winner' : getattr(currentGame, 'winner'),
            'pick' : currentPick
        })
    return render(request, 'home/home.html', {'gameData': gameData, 'userLeagues': userLeagues, 'leagueUsers': leagueUsers, 'activeLeague': activeLeague.name})