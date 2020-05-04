from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from league import utils as leagueUtils
from league.models import League, Team, LeagueMembership, Season, Week, Game, GameChoice
from account.utils import convertTimeToLocalTimezone
from fantasyFootball import settings
import pytz

# Create your views here.
def default(request):
    return render(request, 'home/welcome.html')
    
@login_required
def dashboard(request, weekId="1", leagueName=""):
    
    #Do a lookup to find all leagues for current user. If none, default to home page with no data
    userLeagues = leagueUtils.getUserLeagues(request.user)
    if userLeagues == None:
        return render(request, 'home/welcome.html')
   
    #Get league passed into view
    activeLeague = leagueUtils.getLeague(leagueName)
    if activeLeague == None:
        #No league found using name passed in, default to user's current active league
        activeLeague = leagueUtils.getUserActiveLeague(request.user)
    else:
        #Set current league to user's active league in Profile
        leagueUtils.setUserActiveLeague(request.user, activeLeague)
    
    #Get current active season
    activeSeason = leagueUtils.getActiveSeason()
    
    #Get all users for active league
    leagueUsers = LeagueMembership.objects.filter(league=activeLeague).order_by('-score')
    
    #Get game data for weekId passed in
    currentWeekGames = Game.objects.filter(week_id=Week.objects.get(id=weekId, season=activeSeason)).order_by('id')
    
    #Initialize empty dictionary for gameData and weeks string list to be passed to template
    gameData = []
    weeks = leagueUtils.getWeekIds()
    
    #Get total number of games for current week and we will count the number of picks the user has made
    gameCount = currentWeekGames.count()
    pickCount = 0
    #We will eventually want to get the currentdate and compare it to the week start date and only grab that week
    for currentGame in currentWeekGames:
        #Check to see if there is pick data for this game
        try:
            currentGamePick = GameChoice.objects.get(league=activeLeague,user=request.user,week=Week.objects.get(id=weekId, season=activeSeason),game=currentGame).pickWinner
            if currentGamePick:
                currentPick = currentGamePick
                pickCount += 1
                upcomingPickWarning = False
            else: #If we get here it means that the user has made a bet selection, but not a pick selection
                currentPick = None
                 #User has not yet made a pick, let's warn them if the game is going to lock soon. ( -6 hours -----if current time is here, warn user---- -3 hours ------ Game time)
                if currentGame.dateTime - timedelta(hours=12) < datetime.utcnow().replace(tzinfo=pytz.utc) < currentGame.dateTime - timedelta(hours=1):
                    upcomingPickWarning = True
                else:
                    upcomingPickWarning = False
        except:
            #User has not yet made a pick, let's warn them if the game is going to lock soon. ( -6 hours -----if current time is here, warn user---- -3 hours ------ Game time)
            if currentGame.dateTime - timedelta(hours=12) < datetime.utcnow().replace(tzinfo=pytz.utc) < currentGame.dateTime - timedelta(hours=1):
                upcomingPickWarning = True
            else:
                upcomingPickWarning = False
            currentPick = None

        #Check if the game is in progress
        if currentGame.dateTime < datetime.utcnow().replace(tzinfo=pytz.utc) < currentGame.dateTime + timedelta(hours=3): #This is assuming the game will be 3 hours or less
            gameActive = True
        else:
            gameActive = False

        gameData.append(
        {
            'game' : currentGame,
            'date' : datetime.strftime(convertTimeToLocalTimezone(request.user, currentGame.dateTime), '%b %#d, %Y'),
            'time' : datetime.strftime(convertTimeToLocalTimezone(request.user, currentGame.dateTime), '%#I:%M %p'),
            'pick' : currentPick,
            'upcomingPickWarning' : upcomingPickWarning,
            'gameActive' : gameActive
        })

    return render(request, 'home/dashboard.html', 
    {
        'gameData': gameData, 
        'userLeagues': userLeagues, 
        'leagueUsers': leagueUsers, 
        'activeLeague': activeLeague.name, 
        'week': weekId,
        'weeks': weeks,
        'gameCount': gameCount,
        'pickCount': pickCount
    })

def welcome(request):
    return render(request, 'home/welcome.html')