from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice, Team
from league import utils as leagueUtils
from account.utils import convertTimeToLocalTimezone

# Create your views here.
@login_required
def picks(request, weekId="1", leagueName=""):
    if request.method == "POST":

        #Do a lookup to find all leagues for current user
        userLeagues = leagueUtils.getUserLeagues(request.user)
        if userLeagues == None:
            return render(request, 'home/welcome.html')

        pickData = request.POST
        try:
            #Get active season
            activeSeason = Season.objects.get(active=True)
            #If this creates an error, it is because no week with this id is in the database
            currentWeek = Week.objects.get(id=weekId, season=activeSeason)
        except:
            #Return user to home page, SEND ADMIN email that this happened.
            print("No week/season combo with id " + weekId + "/" + activeSeason.year + " exists in the db.")
            return render(request, 'home/home.html')

        #Check if week is locked (It shouldn't be, this is someone trying to be sneaky)
        if currentWeek.picksLocked == True:
            return render(request, 'picks/picks.html')
        
        #Get user's active league to apply picks to
        activeLeague = leagueUtils.getUserActiveLeague(request.user)
        
        #Get week game data from current week
        games = Game.objects.filter(week=currentWeek).order_by('id')

        for currentPick in pickData:    #This is assuming the games and picks are in the same order
            if currentPick != "csrfmiddlewaretoken":
                currentGame = Game.objects.get(id=currentPick, week=currentWeek)
                print(currentGame.homeTeam.name + " VS " + currentGame.awayTeam.name)
                winnerPicked = Team.objects.get(name=pickData[currentPick])
                print("Winner picked: " + winnerPicked.name)

                #Check to see if there is already a pick for this game
                existingPick = GameChoice.objects.filter(league=activeLeague,user=request.user,week=currentWeek,game=currentGame)
                
                if existingPick:
                    existingPick[0].pickWinner = winnerPicked
                    existingPick[0].save()
                else:    
                    #Save gamechoice object using currentGame, currentLeague and user
                    currentWinnerPick = GameChoice(
                        user=request.user,
                        league=activeLeague,
                        game = currentGame,
                        week = currentWeek,
                        pickWinner = winnerPicked
                    )
                    currentWinnerPick.save()
        #Generate pick page with current week and current league
        redirectUrl = '/picks/' + str(currentWeek.id) + '/' + activeLeague.name
        return redirect(redirectUrl)
    
    elif request.method == "GET":
        #Do a lookup to find all leagues for current user
        userLeagues = leagueUtils.getUserLeagues(request.user)
        if userLeagues == None:
            return render(request, 'home/welcome.html')

        #Try to set active league to leagueName passed in, otherwise use active league
        try:
            activeLeague = League.objects.get(name=leagueName)
            leagueUtils.setUserActiveLeague(activeLeague)
        except:
            activeLeague = leagueUtils.getUserActiveLeague(request.user)
        
        #Initialize empty dictionary for gameData to be passed to template
        pickData = []
        
        #Get current week in active season
        currentWeek = Week.objects.get(id=weekId, season=Season.objects.get(active=True))

        #Get all games from current week for current league
        currentWeekGames = Game.objects.filter(week=currentWeek).order_by('id')
        for currentGame in currentWeekGames:
            
            #Query for game choice model
            try:
                currentGameChoice = GameChoice.objects.get(league=activeLeague,user=request.user,week=currentWeek,game=currentGame)
                winnerSelected = currentGameChoice.pickWinner
            except:
                winnerSelected = None #default pick to none until they have made one

            pickData.append(
            {
                'game' : currentGame.id,
                'homeTeam' : currentGame.homeTeam,
                'homeScore' : currentGame.homeScore,
                'awayTeam' : currentGame.awayTeam,
                'awayScore' : currentGame.awayScore,
                'date' : datetime.strftime(convertTimeToLocalTimezone(request.user, currentGame.dateTime), '%b %#d, %Y'),
                'time' : datetime.strftime(convertTimeToLocalTimezone(request.user, currentGame.dateTime), '%#I:%M %p'),
                'pick' : winnerSelected,
                'pickLocked' : currentGame.pickLocked
            })

        weeks = leagueUtils.getWeekIds()
        
        return render(request, 'picks/picks.html', {'pickData': pickData, 'userLeagues': userLeagues, 'currentWeek': currentWeek, 'activeLeague': activeLeague, 'weeks': weeks})