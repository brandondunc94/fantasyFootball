from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice
from league.utils import getUserLeagues
import json

# Create your views here.
def command(request):
    if request.method == "POST":
        return render(request, 'command/command.html')
    elif request.method == "GET":
        return render(request, 'command/command.html')

def lockWeek(request, weekId):
    #Get week and set flag so that picks are locked in for this given week
    currentWeek = Week.objects.get(id=weekId)
    currentWeek.picksLocked = True
    currentWeek.save()
    return render(request, 'command/command.html')

def scoreWeek(request, weekId, seasonYear="20192020"):
    
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

def createSeason(request):

    #Create new season object in db
    season = Season(year="20192020")
    season.save()
    #season = Season.objects.get(year="20192020")

    #Open team info JSON file
    with open('./static/teams.json', 'r') as teamFile:
        teams = json.load(teamFile)
        teamFile.close()

    #Open current season JSON file
    with open('./static/season20192020.json', 'r') as seasonFile:
        seasonData = json.load(seasonFile)
    
    for week in seasonData:
        newWeek = Week(season=season)
        newWeek.save()
        for game in week['games']:
            homeTeamName = game['homeTeamData']['homeTeam']
            awayTeamName = game['awayTeamData']['awayTeam']
            awayTeamData = next(item for item in teams if item['name'] == awayTeamName)
            homeTeamData = next(item for item in teams if item['name'] == homeTeamName)
            newGame = Game(
                week=newWeek, 
                homeTeam = homeTeamName, 
                homeCity = homeTeamData['city'],
                awayTeam = awayTeamName,
                awayCity = awayTeamData['city'],
                homeScore = game['homeTeamData']['score'],
                awayScore = game['awayTeamData']['score'],
                winner = game['winner'],
                loser = game['loser'],
                location = game['location']
                )    
            newGame.save()

    seasonFile.close()
    return render(request, 'command/command.html')