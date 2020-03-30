from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice
from league.utils import getUserLeagues
import json, smtplib, ssl
from datetime import datetime
from django.http import JsonResponse

# Create your views here.
def commandHome(request):
    
    #Get seasons
    seasons = Season.objects.all()

    return render(request, 'command/command.html', {'seasons': seasons})

def seasonSettings(request, seasonYear=""):

    season = Season.objects.get(year=seasonYear)

    return render(request, 'command/seasonSettings.html', {'season': season})

def gameOptionsPage(request, seasonYear="2019-2020", weekId="1"):

    #Get season object for season passed in
    season = Season.objects.get(year=seasonYear)
    #Try to fetch all games for week and season passed in
    currentWeek = Week.objects.get(id=weekId, season=season)

    #Get game data for weekId passed in
    currentWeekGames = Game.objects.filter(week=currentWeek)
    
    #Initialize empty dictionary for gameData to be passed to template
    gameData = []

    #We will eventually want to get the currentdate and compare it to the week start date and only grab that week
    for currentGame in currentWeekGames:
        #dateFormatted = datetime.strptime(getattr(currentGame, 'date'), '%y
        gameData.append(
        {
            'homeTeam' : getattr(currentGame, 'homeTeam'),
            'homeScore' : getattr(currentGame, 'homeScore'),
            'awayTeam' : getattr(currentGame, 'awayTeam'),
            'awayScore' : getattr(currentGame, 'awayScore'),
            'date' : getattr(currentGame, 'date'),
            'id' : getattr(currentGame, 'id'),
            'pickLocked' : getattr(currentGame, 'pickLocked')
        })

    return render(request, 'command/gameOptions.html', {'gameData': gameData, 'weekId': weekId, 'season' : season})

def scoreWeek(request, weekId, seasonYear="2019-2020"):
    
    #Get season
    season = Season.objects.get(year=seasonYear)
    week = Week.objects.get(id=weekId, season_id=season.id)

    #Get all leagues
    allLeagues = League.objects.all()
    
    for currentLeague in allLeagues:
        #Get all users in current league
        leagueUsers = LeagueMembership.objects.filter(league=currentLeague)

        for currentMembership in leagueUsers:
            #Get currentUser score
            currentUser = currentMembership.user
            userScore = currentMembership.score
            #Get GameChoices for current user in current league for current week
            weekPicks = GameChoice.objects.filter(league=currentLeague,week=weekId,user=currentUser,)
            for currentPick in weekPicks:
                #Get game data for current game
                currentGame = Game.objects.get(id=currentPick.game_id)

                if currentPick.correctFlag == None:
                    #Check if the winner picked is the same as the winner of the actual game
                    if currentPick.winner == currentGame.winner:
                        #Set correct flag to True
                        currentPick.correctFlag = True
                        userScore += 1
                    else:
                        #Set correct flag to False
                        currentPick.correctFlag = False
                    #Save current pick back to db
                    currentPick.save()
            #Update user score on league membership model
            currentMembership.score = userScore
            currentMembership.save()
    #Get all GameChoice objects for current user, current league, and current week

    return render(request, 'command/command.html')

#AJAX CALL
def saveScore(request):
    seasonYear = request.GET.get('season', None)
    week = request.GET.get('weekId', None)
    game = request.GET.get('gameId', None)
    homeScore = request.GET.get('homeScore', None)
    awayScore = request.GET.get('awayScore', None)

    try:
        #Get season object and then game object for current season, week, and game id
        season = Season.objects.get(year=seasonYear)
        gameObject = Game.objects.get(week= Week.objects.get(season=season,id=week), id=game)

        gameObject.homeScore = homeScore
        gameObject.awayScore = awayScore
        #Convert scores to integers
        homeScore = int(homeScore)
        awayScore = int(awayScore)

        if (homeScore > awayScore):
            gameObject.winner = gameObject.homeTeam
        elif (awayScore > homeScore):
            gameObject.winner = gameObject.awayTeam
        else:
            gameObject.winner = "N/A"

        #Update user scores
        allUsers = User.objects.all()

        for currentUser in allUsers:
            #Get game choices for current game and current user (1 per league that the user is in)
            picks = GameChoice.objects.filter(user=currentUser, game=gameObject)
            
            for currentPick in picks:
                membership = LeagueMembership.objects.get(user=currentUser, league=currentPick.league)

                #Check to see if this game has already been counted towards their score. If so, remove 1 and rescore them
                if currentPick.correctFlag == True:
                    membership.score -= 1
                
                #Give player 1 point if they got this game correct 
                if currentPick.winner == gameObject.winner:
                    currentPick.correctFlag = True
                    membership.score += 1
                else:
                    currentPick.correctFlag = False

                membership.save()
                currentPick.save()

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
    season = Season(year="2019-2020")
    season.save()

    #Open team info JSON file
    with open('./static_in_env/teams.json', 'r') as teamFile:
        teams = json.load(teamFile)
        teamFile.close()

    #Open current season JSON file
    with open('./static_in_env/season20192020.json', 'r') as seasonFile:
        seasonData = json.load(seasonFile)
    try:
        for week in seasonData:
            newWeek = Week(season=season)
            newWeek.save()
            for game in week['games']:
                homeTeamName = game['homeTeamData']['homeTeam']
                awayTeamName = game['awayTeamData']['awayTeam']
                awayTeamData = next(item for item in teams if item['name'] == awayTeamName)
                homeTeamData = next(item for item in teams if item['name'] == homeTeamName)
                try:
                    gameDate = datetime.strptime(game['date'],'%Y%m%d')
                except:
                    gameDate = None

                newGame = Game(
                    week=newWeek, 
                    homeTeam = homeTeamName, 
                    homeCity = homeTeamData['city'],
                    awayTeam = awayTeamName,
                    awayCity = awayTeamData['city'],
                    homeScore = '',
                    awayScore = '',
                    winner = '',
                    loser = '',
                    location = game['location'],
                    date = gameDate
                    )    
                newGame.save()
    except:
        print("Missing data from JSON file, continue processing")
        

    seasonFile.close()
    return render(request, 'command/command.html')

