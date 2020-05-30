from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime, timedelta
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice, Team
from league import utils as leagueUtils
from account.utils import convertTimeToLocalTimezone, getUserScore

#AJAX CALL - This view is called in a loop up to 16 times for a given week
def save_bets(request):
    status = False
    try:    #Retrieve league, week, game, and team objects
        league = League.objects.get(name=request.GET.get('leagueName', None))
        week = Week.objects.get(id=request.GET.get('weekId', None))
        game = Game.objects.get(id=request.GET.get('gameId', None))
        
        try:
            pick = Team.objects.get(name=request.GET.get('pick'))
            betAmount = request.GET.get('betAmount', None)
        except:
            pick = None #User is removing their pick, setting pick to None
            betAmount = 0

        try:
            #Check to see if there is already a pick for this game
            existingPick = GameChoice.objects.get(league=league,user=request.user,week=week,game=game)
            existingPick.betWinner = pick
            existingPick.betAmount = betAmount
            existingPick.save()
        except:
            #Save gamechoice object using currentGame, currentLeague and user
            currentWinnerPick = GameChoice(
                user=request.user,
                league= league,
                game = game,
                week = week,
                betWinner = pick,
                betAmount = betAmount
            )
            currentWinnerPick.save()
        status = True
    except:
        print("Could not retrieve the league, week, game, or team when trying to save the bet.")
        status = False
    
    data = {
            'status': status
        }

    return JsonResponse(data)