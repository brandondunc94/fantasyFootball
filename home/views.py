from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
import json
from league import utils as leagueUtils
from league.models import League, Team, LeagueMembership, Season, Week, Game, GameChoice
from account.models import Profile
from datetime import datetime, timedelta

# Create your views here.
@login_required
def home(request, weekId="1", leagueName=""):

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
    
    #Get current active season
    activeSeason = Season.objects.get(active=True)

    #Get all users for active league
    leagueUsers = LeagueMembership.objects.filter(league=activeLeague).order_by('-score')
    
    #Get game data for weekId passed in
    currentWeekGames = Game.objects.filter(week_id=Week.objects.get(id=weekId, season=activeSeason)).order_by('dateTime')
    
    #Initialize empty dictionary for gameData to be passed to template
    gameData = []
    gameCount = currentWeekGames.count()
    pickCount = 0
    #We will eventually want to get the currentdate and compare it to the week start date and only grab that week
    for currentGame in currentWeekGames:
        #Check to see if there is pick data for this game
        try:
            currentGamePick = GameChoice.objects.get(league=activeLeague,user=request.user,week=Week.objects.get(id=weekId, season=activeSeason),game=currentGame)
            currentPick = currentGamePick.winner
            pickCount += 1
        except:
            currentPick = None

        gameData.append(
        {
            'homeTeam' : currentGame.homeTeam,
            'homeScore' : currentGame.homeScore,
            'awayTeam' : currentGame.awayTeam,
            'awayScore' : currentGame.awayScore,
            'winner' : currentGame.winner,
            'date' : datetime.strftime(currentGame.dateTime, '%b %#d, %Y'),
            'time' : datetime.strftime(currentGame.dateTime - timedelta(hours=7), '%#I:%M %p'),
            'pick' : currentPick
        })

    return render(request, 'home/home.html', 
    {
        'gameData': gameData, 
        'userLeagues': userLeagues, 
        'leagueUsers': leagueUsers, 
        'activeLeague': activeLeague.name, 
        'week': weekId,
        'gameCount': gameCount,
        'pickCount': pickCount
    })

def welcome(request):
    return render(request, 'home/welcome.html')