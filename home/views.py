from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from league import utils as leagueUtils
from league.models import League, Team, LeagueMembership, Season, Week, Game, GameChoice, LeagueMessage, LeagueNotification, LeagueMembershipRequest
from bets.utils import determineCorrectBetFlag
from account.utils import convertTimeToLocalTimezone, getUserProfile
from fantasyFootball import settings
import pytz

@login_required
def dashboard(request, weekId='', leagueName=''):
    
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
    
    #Get current active season and active week
    activeSeason = leagueUtils.getActiveSeason()
    if weekId == '': #Use weekId passed in if user wants to view a different week than the active week
        weekId = leagueUtils.getActiveWeekId()

    #Get all users for active league
    leagueMembers = LeagueMembership.objects.filter(league=activeLeague).order_by('-score')
    leagueUserData = []

    #Create json list of users and their weekly scores
    for currentUserMembership in leagueMembers:

        #Split weeklyScores by comma
        weeklyScores = currentUserMembership.weeklyScores.rstrip(',').split(',')
        
        try: #Get current week score change
            weeklyGain = currentUserMembership.score - int(weeklyScores[-1])
        except:
            weeklyGain = 0
        
        try: #Calculate user pick percentage
            pickPercentage = round(currentUserMembership.correctPicks/activeSeason.gameCount,2)
        except:
            pickPercentage = 0

        weeklyScores.append(str(currentUserMembership.score))
        leagueUserData.append(
        {
            'totalScore': currentUserMembership.score,
            'weeklyScores': weeklyScores,
            'username': currentUserMembership.user.username,
            'weeklyGain': weeklyGain,
            'pickPercentage': pickPercentage
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
            'notificationType': currentNotification.notificationType
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
        currentWeekGames = Game.objects.filter(week_id=Week.objects.get(id=weekId, season=activeSeason)).order_by('dateTime')
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
        'userScore': userScore
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
        except:
            currentGameChoice = None

        if currentGame.pickLocked:
            inProgressCorrectBetFlag = determineCorrectBetFlag(game=currentGame,gameChoice=currentGameChoice)
        else:
            inProgressCorrectBetFlag = False
            
        gameData.append(
        {
            'game' : currentGame,
            'date' : datetime.strftime(convertTimeToLocalTimezone(request.user, currentGame.dateTime), '%a %m/%d/%y'),
            'time' : datetime.strftime(convertTimeToLocalTimezone(request.user, currentGame.dateTime), '%#I:%M %p'),
            'gameChoice' : currentGameChoice,
            'inProgressCorrectBetFlag': inProgressCorrectBetFlag,
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
        'leagueRequests': leagueRequests
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
