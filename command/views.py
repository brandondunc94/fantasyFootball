from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from league.models import League, LeagueMembership, Season, Week, Game, Team, GameChoice
from league.utils import getUserLeagues, createLeagueNotification
import json, smtplib, ssl
from datetime import datetime
import pytz
from django.http import JsonResponse

# Create your views here.
@staff_member_required
def commandHome(request):
    #Get seasons
    seasons = Season.objects.all()

    return render(request, 'command/command.html', {'seasons': seasons})

@staff_member_required
def seasonSettings(request, seasonYear=""):

    season = Season.objects.get(year=seasonYear)
    teams = Team.objects.all()
    weeks = Week.objects.filter(season=season)

    return render(request, 'command/seasonSettings.html', {'season': season, 'teams': teams, 'weeks': weeks})

@staff_member_required
def gameOptionsPage(request, seasonYear="2019-2020", weekId="1"):

    #Get season object for season passed in
    season = Season.objects.get(year=seasonYear)

    #Get all weeks for current season
    weeks = Week.objects.filter(season=season)

    #Try to fetch all games for week and season passed in
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

    return render(request, 'command/gameOptions.html', {'gameData': gameData, 'weekId': weekId, 'season' : season, 'weeks': weeks})

def leagueManage(request):
    leagues = League.objects.all()
    return render(request, 'command/leagueManage.html', {'leagues': leagues})

#AJAX CALL
def saveScoreSpread(request):
    seasonYear = request.GET.get('season', None)
    week = request.GET.get('weekId', None)
    game = request.GET.get('gameId', None)
    homeScore = request.GET.get('homeScore', None)
    awayScore = request.GET.get('awayScore', None)
    homeSpread = request.GET.get('homeSpread', None)
    awaySpread = request.GET.get('awaySpread', None)

    try:
        #Get season object and then game object for current season, week, and game id
        season = Season.objects.get(year=seasonYear)
        gameObject = Game.objects.get(week= Week.objects.get(season=season,id=week), id=game)

        if gameObject.winner == None: #Only score game if it hasnt already been scored
            #Update scores if passed in and score players
            try:
                homeScore = int(homeScore)
                awayScore = int(awayScore)
            except:
                homeScore = None
                awayScore = None

            if homeScore and awayScore:
                gameObject.homeScore = homeScore
                gameObject.awayScore = awayScore

                if (homeScore > awayScore):
                    gameObject.winner = gameObject.homeTeam
                    gameObject.homeTeam.wins += 1
                    gameObject.awayTeam.losses += 1
                elif (awayScore > homeScore):
                    gameObject.winner = gameObject.awayTeam
                    gameObject.homeTeam.losses += 1
                    gameObject.awayTeam.wins += 1
                else:
                    gameObject.winner = None
                
                #Save home and away wins/losses update, save gameObject changes
                gameObject.homeTeam.save()
                gameObject.awayTeam.save()

                #Update user scores
                allUsers = User.objects.all()   #Get all users

                for currentUser in allUsers:
                    #Get game choices for current game and current user (1 per league that the user is in)
                    picks = GameChoice.objects.filter(user=currentUser, game=gameObject)
                    
                    for currentPick in picks:
                        membership = LeagueMembership.objects.get(user=currentUser, league=currentPick.league)
                        
                        if currentPick.scoredFlag == None: #This game choice has not yet been scored
                            currentPick.scoredFlag = True #Mark this game as scored
                            #Give player 50 points if they got this game correct 
                            if currentPick.pickWinner == gameObject.winner:
                                membership.score += 50
                                currentPick.correctPickFlag = True

                            #Check if spread bet was correct and give points accordingly
                            if currentPick.betWinner:
                                if currentPick.betWinner == gameObject.homeTeam: #User selected home team spread
                                    if gameObject.homeSpread < gameObject.awaySpread: #Home Team was supposed to win
                                        if gameObject.homeScore - gameObject.awayScore >= gameObject.awaySpread: #Home team won by their spread, pay player
                                            currentPick.amountWon += currentPick.betAmount * .9
                                            membership.score += currentPick.amountWon
                                            currentPick.correctBetFlag = True
                                        else:   #Home team did not win by their spread, take player's points
                                            currentPick.amountWon -= currentPick.betAmount
                                            membership.score += currentPick.amountWon #This will be negative
                                            currentPick.correctBetFlag = False
                                    elif gameObject.awaySpread < gameObject.homeSpread: #Home team was supposed to lose
                                        if gameObject.awayScore - gameObject.homeScore <= gameObject.homeSpread: #Home team lost within their spread margin or won, pay player
                                            currentPick.amountWon += currentPick.betAmount * .9
                                            membership.score += currentPick.amountWon
                                            currentPick.correctBetFlag = True
                                        else:   #Home team lost by too many points, take player's points
                                            currentPick.amountWon -= currentPick.betAmount
                                            membership.score += currentPick.amountWon #This will be negative
                                            currentPick.correctBetFlag = False
                                else: #User selected away team spread
                                    if gameObject.awaySpread < gameObject.homeSpread: #Away Team was supposed to win
                                        if gameObject.awayScore - gameObject.homeScore >= gameObject.homeSpread: #Away team won by their spread, pay player
                                            currentPick.amountWon += currentPick.betAmount * .9
                                            membership.score += currentPick.amountWon
                                            currentPick.correctBetFlag = True
                                        else:   #Away team did not win by their spread, take player's points
                                            currentPick.amountWon -= currentPick.betAmount
                                            membership.score += currentPick.amountWon #This will be negative
                                            currentPick.correctBetFlag = False
                                    elif gameObject.homeSpread < gameObject.awaySpread: #Away team was supposed to lose
                                        if gameObject.homeScore - gameObject.awayScore <= gameObject.awaySpread: #Away team lost within their spread margin or won, pay player
                                            currentPick.amountWon += currentPick.betAmount * .9
                                            membership.score += currentPick.amountWon
                                            currentPick.correctBetFlag = True
                                        else:   #Away team lost by too many points, take player's points
                                            currentPick.amountWon -= currentPick.betAmount
                                            membership.score += currentPick.amountWon #This will be negative
                                            currentPick.correctBetFlag = False
                                if currentPick.amountWon > 100:
                                    #Player scored a boat load of points, create a league notification about it
                                    message = 'Score Update - ' + currentUser.username + " scored " + str(int(currentPick.amountWon)) + " points by betting on the " + currentPick.betWinner.name + "!"
                                    createLeagueNotification(currentPick.league.name, message)
                                    
                        membership.save()
                        currentPick.save()
        
        #Update spreads if they were passed in
        try:    #Convert spreads to integers
            homeSpread = int(homeSpread)
            awaySpread = int(awaySpread)
        except:
            homeSpread = None
            awaySpread = None
        
        #Update game spreads
        if homeSpread and awaySpread:
            gameObject.homeSpread = homeSpread
            gameObject.awaySpread = awaySpread

        #Save game object changes (scores and spreads)
        gameObject.save()

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

def createSeason(request):

    #Create new season object in db
    try:
        season = Season(year="2020-2021")
        season.save()
    except:
        print("Season already exists, continuing..")

    #Populate db with team data
    try:
        createTeams(season)
    except:
        print("Teams have already been populated, continuing...")

    #Open current season JSON file
    with open('./static_in_env/season20192020.json', 'r') as seasonFile:
        seasonData = json.load(seasonFile)
    
    #Initialize timezone to US/Pacific. This is the time zone used on the season json file
    pst = pytz.timezone('US/Pacific')

    try:
        for week in seasonData:
            newWeek = Week(season=season)
            newWeek.save()
            for game in week['games']:
                homeTeam = Team.objects.get(name=game['homeTeam'])
                awayTeam = Team.objects.get(name=game['awayTeam'])
                try:
                    gameDateTime = datetime.strptime(game['date'],'%Y%m%d %I:%M %p')

                    #Add US/Pacific timezone to gameDateTime since it is originally a naive datetime object
                    gameDateTime = pst.localize(gameDateTime)
                    gameDateTime = gameDateTime.astimezone(pytz.utc) #Convert to utc before storing in database

                except:
                    gameDateTime = None

                newGame = Game(
                    week=newWeek, 
                    homeTeam = homeTeam, 
                    awayTeam = awayTeam,
                    homeScore = '',
                    awayScore = '',
                    location = game['location'],
                    dateTime = gameDateTime,
                    winner = None,
                    loser =None
                    )    
                newGame.save()
    except:
        print("Something happened while creating new season. Check the season JSON file for missing data?")

    seasonFile.close()
    return render(request, 'command/command.html')

def createTeams(season):

    #Open team info JSON file
    with open('./static_in_env/teams.json', 'r') as teamFile:
        teams = json.load(teamFile)
        teamFile.close()
    
    for currentTeam in teams:
        newTeam = Team(
            name = currentTeam['name'],
            city = currentTeam['city'],
            wins = 0,
            losses = 0,
            season = season
        )
        newTeam.save()

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
    seasonYear = request.GET.get('seasonYear', None)
    weekId = request.GET.get('weekId', None)
    homeTeamName = request.GET.get('homeTeam', None)
    awayTeamName = request.GET.get('awayTeam', None)
    gameDate = request.GET.get('gameDate', None)
    gameTime = request.GET.get('gameTime', None)
    try:
        #Get team objects
        homeTeam = Team.objects.get(name=homeTeamName)
        awayTeam = Team.objects.get(name=awayTeamName)

        #Get week object
        season = Season.objects.get(year=seasonYear)
        week = Week.objects.get(id=weekId, season=season)

        #Convert gameDateTime to a datetime object
        gameDateTimeString = gameDate + " " + gameTime
        gameDateTime = datetime.strptime(gameDateTimeString,'%Y-%m-%d %H:%M')

        #Add US/Pacific timezone to gameDateTime since it is originally a naive datetime object
        pst = pytz.timezone('US/Pacific')
        gameDateTime = pst.localize(gameDateTime)
        
        gameDateTime = gameDateTime.astimezone(pytz.utc) #Convert to utc before storing in database
        
        newGame = Game( week=week, homeTeam=homeTeam, awayTeam=awayTeam, dateTime=gameDateTime)
        newGame.save()
        status = True
    except:
        print("Unable to create new game.")
        status = False

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