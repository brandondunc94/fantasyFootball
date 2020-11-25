from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
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

def compare_teams(request, homeTeamName, awayTeamName):

    #Get each team
    
    homeTeam = Team.objects.get(name = homeTeamName)
    awayTeam = Team.objects.get(name = awayTeamName)

    homeTeamData = {}

    homeGames = Game.objects.filter(Q(homeTeam=homeTeam) | Q(awayTeam=homeTeam))
    homeCoveredSpread = homeGames.filter(spreadWinner=homeTeam).count()
    homeCoveredSpreadPercentage = "{:.1%}".format(homeCoveredSpread/homeGames.count())
    #Get stats of each team
    homeTeamData = (
    {
        'homeGames' : homeGames,
        'homeTeam': homeTeam,
        'homeTeamName': homeTeamName,
        'homeCoveredSpread': homeCoveredSpread,
        'homeCoveredSpreadPercentage': homeCoveredSpreadPercentage,
    })

    awayTeamData = {}

    awayGames = Game.objects.filter(Q(homeTeam=awayTeam) | Q(awayTeam=awayTeam))
    awayCoveredSpread = awayGames.filter(spreadWinner=awayTeam).count()
    awayCoveredSpreadPercentage = "{:.1%}".format(awayCoveredSpread/awayGames.count())

    awayTeamData = (
    {
        'awayGames' : awayGames,
        'awayTeam' : awayTeam,
        'awayTeamName': awayTeamName,
        'awayCoveredSpread': awayCoveredSpread,
        'awayCoveredSpreadPercentage': awayCoveredSpreadPercentage,
    })

    return render(request, 'picks/teamCompare.html', {
        'homeTeamData': homeTeamData,
        'awayTeamData': awayTeamData,
    })
