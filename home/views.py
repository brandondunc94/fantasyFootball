from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
import json
#from home import classes

# Create your views here.
@login_required
def home(request):
    #Get all leagues and display current stats based on picks
    with open('./static/teams.json', 'r') as teamFile:
        teams = json.load(teamFile)
        teamFile.close()
    #Open file for current season, we will eventually want to get the 
    #currentdate and compare it to the week start date and only grab that week
    with open('./static/season20192020.json', 'r') as seasonFile:
        season = json.load(seasonFile)
        for week in season['weeks']:
            for game in week['games']:

                homeTeamName = game['homeTeamData']['homeTeam']
                awayTeamName = game['awayTeamData']['awayTeam']
                #currentHomeCity = [m['name'] for m in teams if m['name'] == homeTeamName]
                #currentHomeCity = next(item for item in teams if item['name'] == homeTeamName)

                print(homeTeamName + " VS " + awayTeamName)

        seasonFile.close()
        #Get live scores and display on the top
    return render(request, 'home/home.html')