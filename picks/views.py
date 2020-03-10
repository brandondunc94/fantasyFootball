from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice
from account.models import Profile
from league.utils import getUserLeagues
from picks.forms import PickForm, PickFormSet

# Create your views here.
@login_required
def picks(request):
    if request.method == "POST":
        pickData = request.POST
        #currentWeek = request.POST['week']
        #Determine week number to populate
        week = 1    #defaulting to 1 for now
        currentWeek = Week.objects.get(id=week)
        #Get user league
        currentProfile = Profile.objects.get(user=request.user)
        currentActiveLeague = currentProfile.currentActiveLeague
        
        #Get league from pick list or default to the first league found
        #weekNumber = request.POST.['week']
        #Get week game data from current week
        games = Game.objects.filter(week=currentWeek)
    
        for currentGame, currentPick in zip(games, pickData):    #This is assuming the games and picks are in the same order
            if currentPick != "csrfmiddlewaretoken":
                print(currentGame.homeTeam + " VS " + currentGame.awayTeam)
                print("Winner picked: " + pickData[currentPick])

                #Check to see if there is already a pick for this game
                existingPick = GameChoice.objects.filter(league=currentActiveLeague,user=request.user,week=currentWeek,game=currentGame)
                if existingPick:
                    existingPick[0].winner = pickData[currentPick]
                    existingPick[0].save()
                else:    
                    #Save gamechoice object using currentGame, currentLeague and user
                    currentWinnerPick = GameChoice(
                        user=request.user,
                        league=currentActiveLeague,
                        game = currentGame,
                        week = currentWeek,
                        winner = pickData[currentPick]
                    )
                    currentWinnerPick.save()
        return render(request, 'picks/picks.html')
    elif request.method == "GET":
        
        #Do a lookup to find all leagues for current user
        userLeagues = getUserLeagues(request.user)
        defaultLeague = userLeagues[0]
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
                currentGameChoice = GameChoice.objects.filter(league=defaultLeague,user=request.user,week=week,game=currentGame)
                
                #if winner matches the actual game winner, set correct flag to 'true'
                if currentGameChoice:
                    currentGameChoice = GameChoice.objects.get(game=currentGame, user=request.user)
                    winnerSelected = getattr(currentGameChoice, 'winner')
                else:
                    winnerSelected = None #default pick to none until they have made one

                correctFlag = True #default to true for now
                pickData.append(
                {
                    'game' : currentGame.id,
                    'homeTeam' : getattr(currentGame, 'homeTeam'),
                    'homeScore' : getattr(currentGame, 'homeScore'),
                    'awayTeam' : getattr(currentGame, 'awayTeam'),
                    'awayScore' : getattr(currentGame, 'awayScore'),
                    'correctFlag' : correctFlag,
                    'pick' : winnerSelected
                })
                
                print (currentGameChoice)

            pickFormSet = PickFormSet()
            return render(request, 'picks/picks.html', {'pickData': pickData, 'userLeagues': userLeagues, 'pickFormSet': pickFormSet})