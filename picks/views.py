from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice
from account.models import Profile
from league.utils import getUserLeagues


# Create your views here.
@login_required
def picks(request, weekId="1", leagueName=""):
    if request.method == "POST":

        #Do a lookup to find all leagues for current user
        userLeagues = getUserLeagues(request.user)
        if userLeagues == None:
            return render(request, 'home/home.html')

        pickData = request.POST

        currentWeek = Week.objects.get(id=weekId)

        #Check if week is locked (It shouldn't be, this is someone trying to be sneaky)
        lockedWeek = currentWeek.picksLocked
        if lockedWeek == True:
            return render(request, 'picks/picks.html')
        
        try:
            #Get league from name passed in
            activeLeague = League.objects.get(name=leagueName)
        except:
            #Use first found league
            activeLeague = userLeagues[0]
        
        #Get week game data from current week
        games = Game.objects.filter(week=currentWeek)

        for currentPick in pickData:    #This is assuming the games and picks are in the same order
            if currentPick != "csrfmiddlewaretoken":
                currentGame = Game.objects.get(id=currentPick)
                print(currentGame.homeTeam + " VS " + currentGame.awayTeam)
                print("Winner picked: " + pickData[currentPick])

                #Check to see if there is already a pick for this game
                existingPick = GameChoice.objects.filter(league=activeLeague,user=request.user,week=currentWeek,game=currentGame)
                
                if existingPick:
                    existingPick[0].winner = pickData[currentPick]
                    existingPick[0].save()
                else:    
                    #Save gamechoice object using currentGame, currentLeague and user
                    currentWinnerPick = GameChoice(
                        user=request.user,
                        league=activeLeague,
                        game = currentGame,
                        week = currentWeek,
                        winner = pickData[currentPick]
                    )
                    currentWinnerPick.save()
        #Generate pick page with current week and current league
        redirectUrl = '/picks/' + str(currentWeek.id) + '/' + activeLeague.name
        return redirect(redirectUrl)
    
    elif request.method == "GET":
        #Do a lookup to find all leagues for current user
        userLeagues = getUserLeagues(request.user)
        if userLeagues == None:
            return render(request, 'home/home.html')

        #Try to set active league to leagueName passed in, otherwise use first found
        try:
            activeLeague = League.objects.get(name=leagueName)
        except:
            activeLeague = userLeagues[0]
        
        #Initialize empty dictionary for gameData to be passed to template
        pickData = []
        
        #Get current week
        currentWeek = Week.objects.get(id=weekId)

        #Get all games from current week for current league
        currentWeekGames = Game.objects.filter(week_id=weekId)
        for currentGame in currentWeekGames:
            
            #Query for game choice model
            try:
                currentGameChoice = GameChoice.objects.get(league=activeLeague,user=request.user,week=weekId,game=currentGame)
                winnerSelected = getattr(currentGameChoice, 'winner')
                if winnerSelected == currentGame.winner:
                    correctFlag = True #default to true for now
                else:
                    correctFlag = False
            except:
                winnerSelected = None #default pick to none until they have made one
                correctFlag = None

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

        return render(request, 'picks/picks.html', {'pickData': pickData, 'userLeagues': userLeagues, 'currentWeek': currentWeek, 'activeLeague': activeLeague})