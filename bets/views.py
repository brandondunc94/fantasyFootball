from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice, Team
from league import utils as leagueUtils
from account.utils import convertTimeToLocalTimezone, getUserScore

# Create your views here.
@login_required
def betsHome(request, weekId="1", leagueName=""):
    if request.method == "POST":

        #Do a lookup to find all leagues for current user
        userLeagues = leagueUtils.getUserLeagues(request.user)
        if userLeagues == None:
            return render(request, 'home/welcome.html')

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
            return render(request, 'bets/betsHome.html')
        
        #Get user's active league to apply bets to
        activeLeague = leagueUtils.getUserActiveLeague(request.user)
        
        #Get week game data from current week
        games = Game.objects.filter(week=currentWeek).order_by('id')

        betData = request.POST

        for currentBet in betData:    #This is assuming the games and picks are in the same order
            if (currentBet != "csrfmiddlewaretoken") & (currentBet.startswith('#') == False):
                currentGame = Game.objects.get(id=currentBet, week=currentWeek)
                print(currentGame.homeTeam.name + " VS " + currentGame.awayTeam.name)
                winnerPicked = Team.objects.get(name=betData[currentBet])
                print("Winner picked: " + winnerPicked.name)
                amountBet = betData['#'+currentBet]

                #Check to see if there is already a pick for this game
                existingPick = GameChoice.objects.filter(league=activeLeague,user=request.user,week=currentWeek,game=currentGame)
                
                if existingPick:
                    existingPick[0].betWinner = winnerPicked
                    existingPick[0].betAmount = amountBet
                    existingPick[0].save()
                else:    
                    #Save gamechoice object using currentGame, currentLeague and user
                    currentWinnerPick = GameChoice(
                        user=request.user,
                        league=activeLeague,
                        game = currentGame,
                        week = currentWeek,
                        betWinner = winnerPicked,
                        betAmount = amountBet
                    )
                    currentWinnerPick.save()
        #Generate pick page with current week and current league
        redirectUrl = '/bets/' + str(currentWeek.id) + '/' + activeLeague.name
        return redirect(redirectUrl)
    
    elif request.method == "GET":
        
        #Do a lookup to find all leagues for current user
        userLeagues = leagueUtils.getUserLeagues(request.user)
        if userLeagues == None:
            return render(request, 'home/welcome.html')

        #Try to set active league to leagueName passed in, otherwise use active league in profile
        try:
            activeLeague = League.objects.get(name=leagueName)
            leagueUtils.setUserActiveLeague(activeLeague)
        except:
            activeLeague = leagueUtils.getUserActiveLeague(request.user)
        
        #Initialize empty dictionary for betData to be passed to template
        betData = []
        
        #Get current week in active season
        currentWeek = Week.objects.get(id=weekId, season=Season.objects.get(active=True))

        #Get all games from current week for current league
        currentWeekGames = Game.objects.filter(week=currentWeek).order_by('id')
        for currentGame in currentWeekGames:
            
            #Query for game choice model
            try:
                currentGameChoice = GameChoice.objects.get(league=activeLeague,user=request.user,week=currentWeek,game=currentGame)
                winnerSelected = currentGameChoice.betWinner
                betAmount = currentGameChoice.betAmount
            except:
                winnerSelected = None #default pick to none until they have made one
                betAmount = 0 #default to 0 points bet on current game

            betData.append(
            {
                'game' : currentGame.id,
                'homeTeam' : currentGame.homeTeam,
                'homeScore' : currentGame.homeScore,
                'homeSpread' : currentGame.homeSpread,
                'awayTeam' : currentGame.awayTeam,
                'awayScore' : currentGame.awayScore,
                'awaySpread' : currentGame.awaySpread,
                'date' : datetime.strftime(convertTimeToLocalTimezone(request.user, currentGame.dateTime), '%b %#d, %Y'),
                'time' : datetime.strftime(convertTimeToLocalTimezone(request.user, currentGame.dateTime), '%#I:%M %p'),
                'pick' : winnerSelected,
                'betAmount' : betAmount,
                'pickLocked' : currentGame.pickLocked
            })

        weeks = leagueUtils.getWeekIds()
        userScore = getUserScore(request.user, activeLeague)
        return render(request, 'bets/betsHome.html', {'betData': betData, 'userLeagues': userLeagues, 'currentWeek': currentWeek, 'activeLeague': activeLeague, 'weeks': weeks, 'userScore': userScore})