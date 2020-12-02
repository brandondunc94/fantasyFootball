from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from league.models import League, LeagueMembership, Season, Week, Game, Team, GameChoice
from league.utils import getUserLeagues, createLeagueNotification, getActiveWeekId, createGame, scoreGame, determineWinner, updateGame
from livedata.utils import getWeekSchedule, getInProgressScores, getFinalLiveScores
import json, smtplib, ssl, pytz
from datetime import datetime
from django.http import JsonResponse

# Create your views here.
@staff_member_required
def commandHome(request):
    #Get seasons
    seasons = Season.objects.all()

    return render(request, 'command/command.html', {'seasons': seasons})

@staff_member_required
def seasonSettings(request, seasonYear=''):

    season = Season.objects.get(year=seasonYear)
    teams = Team.objects.all()
    weeks = Week.objects.filter(season=season)

    return render(request, 'command/seasonSettings.html', {'season': season, 'teams': teams, 'weeks': weeks})

@staff_member_required
def gameOptionsPage(request, seasonYear='2019-2020', weekId=''):

    #Get season object for season passed in
    season = Season.objects.get(year=seasonYear)

    #Get all weeks for current season
    weeks = Week.objects.filter(season=season)

    #Get active week if the admin has not passed in a week id
    if weekId == '':
        weekId = getActiveWeekId()
    currentWeek = Week.objects.get(id=weekId, season=season)
    
    #Get game data for weekId passed in
    currentWeekGames = Game.objects.filter(week=currentWeek).order_by('id')
    
    #Initialize empty dictionary for gameData to be passed to template
    gameData = []

    #We will eventually want to get the currentdate and compare it to the week start date and only grab that week
    for currentGame in currentWeekGames:
        #dateFormatted = datetime.strptime(getattr(currentGame, 'date'), '%y
        gameData.append(
        {
            'homeTeam' : currentGame.homeTeam,
            'homeScore' : currentGame.homeScore,
            'homeSpread' : currentGame.homeSpread,
            'awayTeam' : currentGame.awayTeam,
            'awayScore' : currentGame.awayScore,
            'awaySpread' : currentGame.awaySpread,
            'date' : currentGame.dateTime,
            'id' : currentGame.id,
            'pickLocked' : currentGame.pickLocked
        })

    return render(request, 'command/gameOptions.html', {'gameData': gameData, 'currentWeek': currentWeek, 'season' : season, 'weeks': weeks})

@staff_member_required
def leagueManage(request):
    leagues = League.objects.all()
    return render(request, 'command/leagueManage.html', {'leagues': leagues})

#AJAX CALL
def saveScoreSpread(request):
    gameId = request.GET.get('gameId', None)
    homeScore = request.GET.get('homeScore', None)
    awayScore = request.GET.get('awayScore', None)
    homeSpread = request.GET.get('homeSpread', None)
    awaySpread = request.GET.get('awaySpread', None)

    try:
        #Get season object and then game object for current season, week, and game id
        game = Game.objects.get(id=gameId)

        homeScore = int(homeScore)
        awayScore = int(awayScore)

        if game.isComplete == False:
            if homeScore == 0 and awayScore == 0: #This is hoping a game never ends in a 0-0 tie
                gameComplete = False
            else:
                gameComplete = True #Scores provided from admin, game is over

            updateGame(game=game, homeSpread=homeSpread, awaySpread=awaySpread, homeScore=homeScore, awayScore=awayScore, isComplete=gameComplete)

        status = 'SUCCESS'
    except:
        status = 'FAILED'

    data = {
            'status': status
        }

    return JsonResponse(data)

#AJAX CALL
def lockGame(request):
    seasonYear = request.GET.get('seasonYear', None)
    week = request.GET.get('week', None)
    game = request.GET.get('game', None)
    print(seasonYear)
    try:
        #Get season object and then game object for current season, week, and game id
        season = Season.objects.get(year=seasonYear)
        game = Game.objects.get(week= Week.objects.get(season=season,id=week), id=game)
        
        #Lock picks for this game object
        game.pickLocked = True
        game.save()
        status = 'SUCCESS'
    except:
        status = 'FAILED'
    
    data = {
            'status': status
        }

    return JsonResponse(data)

#AJAX CALL
def unlockGame(request):
    seasonYear = request.GET.get('seasonYear', None)
    week = request.GET.get('week', None)
    game = request.GET.get('game', None)
    print(seasonYear)
    try:
        #Get season object and then game object for current season, week, and game id
        season = Season.objects.get(year=seasonYear)
        game = Game.objects.get(week= Week.objects.get(season=season,id=week), id=game)
        
        #Unlock picks for this game object
        game.pickLocked = False
        game.save()
        status = 'SUCCESS'
    except:
        status = 'FAILED'
    
    data = {
            'status': status
        }

    return JsonResponse(data)
    
#AJAX CALL
def addWeek(request):
    seasonYear = request.GET.get('seasonYear', None)
    weekType = request.GET.get('weekType', None)
    
    try:
        #Get season object
        season = Season.objects.get(year=seasonYear)
        newWeek = Week(season=season, altName=weekType)
        newWeek.save()
        status = True
    except:
        print("Season " + seasonYear + " could not be found when trying to create a new week with type " + weekType)
        status = False

    data = {
            'status': status
        }

    return JsonResponse(data)

#AJAX CALL
def addGame(request):
    weekId = request.GET.get('weekId', None)
    homeTeamName = request.GET.get('homeTeam', None)
    awayTeamName = request.GET.get('awayTeam', None)
    gameDate = request.GET.get('gameDate', None)
    gameTime = request.GET.get('gameTime', None)
    homeSpread = request.GET.get('homeSpread', None)
    awaySpread = request.GET.get('awaySpread', None)
    
    status = createGame(weekId=weekId, homeTeamName=homeTeamName,awayTeamName=awayTeamName, gameDate=gameDate, gameTime=gameTime,timezone='US/Pacific', homeSpread=homeSpread, awaySpread=awaySpread)

    data = {
            'status': status
        }

    return JsonResponse(data)

#AJAX CALL
def deleteGame(request):
    seasonYear = request.GET.get('seasonYear', None)
    weekId = request.GET.get('weekId', None)
    gameId = request.GET.get('gameId', None)
    try:
        #Get week object
        season = Season.objects.get(year=seasonYear)
        week = Week.objects.get(pk=weekId, season=season)

        #Get game object
        gameToDelete = Game.objects.get(week=week, id=gameId)
        if gameToDelete.isComplete == False: #Only delete game if its not complete
            gameToDelete.delete()
        status = True
    except:
        status = False

    data = {
            'status': status
        }

    return JsonResponse(data)

#AJAX CALL
def deleteLeague(request):
    leagueName = request.GET.get('leagueName', None)
    try:
        league = League.objects.get(name=leagueName)
        league.delete()
        status = True
    except:
        status = False
        data = {
            'status': status
        }

    return JsonResponse(data)

#AJAX CALL
def activateWeek(request):
    seasonYear = request.GET.get('season', None)
    weekId = request.GET.get('week', None)

    try:
        season = Season.objects.get(year=seasonYear)
        #Unlock specified week and lock all others
        week = Week.objects.get(id=weekId) 
        week.isLocked = False
        week.save()

        #Lock all other weeks
        allOtherWeeks = Week.objects.filter(season=season).exclude(id=weekId)
        for currentWeek in allOtherWeeks:
            currentWeek.isLocked = True
            currentWeek.save()
        
        #Set season's active week
        season.currentActiveWeek = weekId
        season.save()
        status = 'SUCCESS'
    except:
        status = 'FAILED'

    data = {
            'status': status
        }

    return JsonResponse(data)

def recalculatePlayersScores():

    allUsers = User.objects.all()

    for currentUser in allUsers:

        #Get all leagues current user is a part of
        userLeagueMemberships = LeagueMembership.objects.filter(user=currentUser)

        for currentLeagueMembership in userLeagueMemberships:

            #Reset league membership score to 500
            currentLeagueMembership.score = 500

            #Get all league choice objects for current season
            allGameChoices = GameChoice.objects.filter(league=currentLeagueMembership.league, user=currentUser)

            for currentGameChoice in allGameChoices:

                #Add 25 points if pickCorrectFlag == True
                if currentGameChoice.correctPickFlag == True:
                    if currentGameChoice.week_id == 1:
                        currentLeagueMembership.score += 50
                    else:
                        currentLeagueMembership.score += 25
                
                #Add/subtract bet amount won/lost
                currentLeagueMembership.score += currentGameChoice.amountWon
            
            #Save score
            print(currentUser.username + ' score has been recalculated to be ' + str(currentLeagueMembership.score))
            currentLeagueMembership.save()

#AJAX CALL
def getUpcomingWeekSchedule(request):
    try:
        getWeekSchedule()
        status = 'SUCCESS'
    except:
        status = 'FAILED'

    data = {
            'status': status
        }

    return JsonResponse(data)

#AJAX CALL
def getLiveScores(request):
    try:
        getInProgressScores()
        status = 'SUCCESS'
    except:
        status = 'FAILED'

    data = {
            'status': status
        }

    return JsonResponse(data)

#AJAX CALL
def getFinalScores(request):
    try:
        getFinalLiveScores()
        status = 'SUCCESS'
    except:
        status = 'FAILED'

    data = {
            'status': status
        }

    return JsonResponse(data)