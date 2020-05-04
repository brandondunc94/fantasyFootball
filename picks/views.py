from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime, timedelta
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice, Team
from league import utils as leagueUtils
from account.utils import convertTimeToLocalTimezone

# Create your views here.
@login_required
def picks(request, weekId="1", leagueName=""):
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
    
#AJAX CALL - Save single pick
def save_pick(request):
    status = False
    try:    #Retrieve league, week, game, and team objects
        league = League.objects.get(name=request.GET.get('leagueName', None))
        week = Week.objects.get(id=request.GET.get('weekId', None))
        game = Game.objects.get(id=request.GET.get('gameId', None))
        try:
            pick = Team.objects.get(name=request.GET.get('pick'))
        except:
            pick = None #User is removing their pick, setting pick to None

        try:
            #Check to see if there is already a pick for this game
            existingPick = GameChoice.objects.get(league=league,user=request.user,week=week,game=game)
            existingPick.pickWinner = pick
            existingPick.save()
        except:
            #Save gamechoice object using currentGame, currentLeague and user
            currentWinnerPick = GameChoice(
                user=request.user,
                league= league,
                game = game,
                week = week,
                pickWinner = pick
            )
            currentWinnerPick.save()
        status = True
    except:
        print("Could not retrieve the league, week, game, or team when trying to save the pick.")
        status = False
    
    data = {
            'status': status
        }

    return JsonResponse(data)