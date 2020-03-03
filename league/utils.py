from league.models import League, LeagueMembership, Season, Week, Game
from django.contrib.auth.models import User
import json

#Get all leagues for current user
def getUserLeagues(currentUser):
    leagues = []
    memberships = LeagueMembership.objects.filter(user = currentUser)
    for currentMembership in memberships:
        leagues.append(currentMembership.league)
    return(leagues)

def createNewSeason():

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

    
def updateScores():
    #Update score and winner/loser in DB
    return True


