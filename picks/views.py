from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice
from league.utils import getUserLeagues

# Create your views here.
@login_required
def picks(request):
    if request.method == "POST":
        #Get league from pick list or default to the first league found
        
        #Get week from pick list, otherwise default to week 1

        return render(request, 'picks/picks.html')
    elif request.method == "GET":
        
        #Do a lookup to find all leagues for current user
        userLeagues = getUserLeagues(request.user)

        if userLeagues == None:
            return render(request, 'home/home.html')
        else:
            #Initialize empty dictionary for gameData to be passed to template
            pickData = []

            #Determine week number to populate
            week = 1    #defaulting to 1 for now
            #Get all games from current week for current league
            currentWeekGames = Game.objects.filter(week_id=week)
            for currentGame in currentWeekGames:
                
                #Query for game choice model
                currentGameChoice = GameChoice.objects.filter(game=currentGame, user=request.user)

                #if winner matches the actual game winner, set correct flag to 'true'
                if currentGameChoice:
                    winnerSelected = getattr(currentGameChoice, 'winner')
                else:
                    winnerSelected = None #default pick to none until they have made one

                correctFlag = True #default to true for now
                pickData.append(
                {
                    'homeTeam' : getattr(currentGame, 'homeTeam'),
                    'homeScore' : getattr(currentGame, 'homeScore'),
                    'awayTeam' : getattr(currentGame, 'awayTeam'),
                    'awayScore' : getattr(currentGame, 'awayScore'),
                    'correctFlag' : correctFlag
                })
                print (currentGameChoice)
            return render(request, 'picks/picks.html', {'pickData': pickData, 'userLeagues': userLeagues})