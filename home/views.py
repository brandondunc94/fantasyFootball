from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
import json
from league.utils import getUserLeagues
#from home import classes

# Create your views here.
@login_required
def home(request):
    if request.method == "POST":
        #Get league from pick list or default to the first league found
        league = request
        #Get week from pick list, otherwise default to week 1

        return render(request, 'home/home.html')
    elif request.method == "GET":
        #Do a lookup to find all leagues for current user
        userLeagues = getUserLeagues(request.user)

        if userLeagues == None:
            return render(request, 'home/home.html')
        else:
            #Initialize empty dictionary for gameData to be passed to template
            gameData = []

            #Determine week number to populate
            week = 1    #defaulting to 1 for now
    
            #Get all leagues and display current stats based on picks
            with open('./static/teams.json', 'r') as teamFile:
                teams = json.load(teamFile)
                teamFile.close()
            #Open file for current season, we will eventually want to get the 
            #currentdate and compare it to the week start date and only grab that week
            with open('./static/season20192020.json', 'r') as seasonFile:
                season = json.load(seasonFile)
                #Get week JSON object
                displayWeek = next(item for item in season if item['id'] == week)
                for game in displayWeek['games']:
                    homeTeamName = game['homeTeamData']['homeTeam']
                    awayTeamName = game['awayTeamData']['awayTeam']
                    awayTeamProfile = next(item for item in teams if item['name'] == awayTeamName)
                    homeTeamProfile = next(item for item in teams if item['name'] == homeTeamName)
                        
                    gameData.append(
                        {
                            'homeTeam' : homeTeamProfile, 
                            'awayTeam' : awayTeamProfile,
                            'homeScore' : game['homeTeamData']['score'],
                            'awayScore' : game['awayTeamData']['score'],
                            'location' : game['location'],
                            'date' : game['date']
                        })

                    print(homeTeamName + " VS " + awayTeamName)

            seasonFile.close()
                #Get live scores and display on the top
            return render(request, 'home/home.html', {'gameData': gameData, 'userLeagues': userLeagues})