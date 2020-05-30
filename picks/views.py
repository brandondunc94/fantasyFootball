from django.contrib.auth.models import User
from django.http import JsonResponse
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice, Team

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