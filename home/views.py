from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from league import utils as leagueUtils
from league.models import League, Team, LeagueMembership, Season, Week, Game, GameChoice, LeagueMessage, LeagueNotification, LeagueMembershipRequest
from account.utils import convertTimeToLocalTimezone, getUserProfile
from fantasyFootball import settings
import pytz

@login_required
def dashboard(request, weekId="3", leagueName=""):
    
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
    leagueMembers = LeagueMembership.objects.filter(league=activeLeague).order_by('-score')
    leagueUserData = []
    #Create json list of users and their weekly scores
    for currentUserMembership in leagueMembers:

        #Split weeklyScores by comma
        weeklyScores = currentUserMembership.weeklyScores.rstrip(',').split(',')
        weeklyScores.append(str(currentUserMembership.score))
        try:
            weeklyGain = currentUserMembership.score - int(weeklyScores[-1])
        except:
            weeklyGain = 0
        leagueUserData.append(
        {
            'totalScore': currentUserMembership.score,
            'weeklyScores': weeklyScores,
            'username': currentUserMembership.user.username,
            'weeklyGain': weeklyGain
        })


    #Get all league messages, notifications and convert the date/times to user's timezone
    leagueMessages = []
    leagueNotifications = []

    leagueMessagesObjects = LeagueMessage.objects.filter(league=activeLeague)
    leagueNotificationsObjects = LeagueNotification.objects.filter(league=activeLeague).order_by('-createDate')

    for currentMessage in leagueMessagesObjects:
        messageDateTime = convertTimeToLocalTimezone(request.user, currentMessage.createDate)
        leagueMessages.append(
        {
            'createDate': messageDateTime,
            'message': currentMessage.message,
            'username': currentMessage.user.username
        })
    for currentNotification in leagueNotificationsObjects:
        notificationDateTime = convertTimeToLocalTimezone(request.user, currentNotification.createDate)
        leagueNotifications.append({
            'createDate': notificationDateTime,
            'message': currentNotification.message,
        })

    #Get user score from league membership
    userScore = LeagueMembership.objects.get(league=activeLeague, user=request.user).score

    #Determine if user is the league admin and get league join requests
    if request.user == activeLeague.admin:
        isAdmin = True
        #Get league membership requests if the league is private
        if activeLeague.isPublic == False:
            leagueRequests = LeagueMembershipRequest.objects.filter(league=activeLeague)
        else:
            leagueRequests = None
    else:
        isAdmin = False
        leagueRequests = None

    #Get game data for weekId passed in
    try:
        currentWeekGames = Game.objects.filter(week_id=Week.objects.get(id=weekId, season=activeSeason)).order_by('dateTime').order_by('id')
    except:
        #No games are currently available. Open up the home page with no data.
        #THIS SHOULD BE A HOME PAGE FOR OFFSEASON
        return render(request, 'home/dashboard.html', {
        'userLeagues': userLeagues,
        'leagueUserData': leagueUserData, 
        'activeLeague': activeLeague.name,
        'leagueMessages': leagueMessages,
        'leagueNotifications': leagueNotifications,
        'leagueRequests': leagueRequests,
        'userScore': userScore,
        'page': 'dashboard'
    })

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
            currentGameChoice = GameChoice.objects.get(league=activeLeague,user=request.user,week=Week.objects.get(id=weekId, season=activeSeason),game=currentGame)
            if currentGameChoice.pickWinner:
                pickCount += 1
                upcomingPickWarning = False
            else: #If we get here it means that the user has not yet made a pick selection
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
            currentGameChoice = None

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
            'gameChoice' : currentGameChoice,
            'upcomingPickWarning' : upcomingPickWarning,
            'gameActive' : gameActive
        })

    #Template always expects {week}, {weeks}, {activeLeague}, {userLeagues}
    return render(request, 'home/dashboard.html', 
    {
        'gameData': gameData, 
        'userLeagues': userLeagues,
        'userScore': userScore,
        'isAdmin': isAdmin,
        'leagueUserData': leagueUserData, 
        'activeLeague': activeLeague.name, 
        'week': weekId,
        'weeks': weeks,
        'gameCount': gameCount,
        'pickCount': pickCount,
        'leagueMessages': leagueMessages,
        'leagueNotifications': leagueNotifications,
        'leagueRequests': leagueRequests,
        'lastAccessedPage': getUserProfile(request.user).lastPageAccessed,
        'page': 'dashboard'
    })

def redirect_home(request):
    if request.user.is_authenticated:
        return dashboard(request)
    else:
        response = redirect('/login/')
        return response

def about(request):
    return render(request, 'home/about.html')

def welcome(request):
    return render(request, 'home/welcome.html')