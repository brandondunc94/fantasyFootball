from __future__ import absolute_import, unicode_literals

from celery import shared_task
from league.models import Season, Week, Game
from datetime import datetime, timedelta

@shared_task
def lockPicks():
    try:
        #Get current active season
        activeSeason = Season.objects.get(active=True)
    except:
        #Season has not been created, just quit this task
        return True

    #Get all games that 
    upcomingGames = Game.objects.filter(dateTime__range=[datetime.now(), datetime.now() + timedelta(hours=3)])

    for game in upcomingGames:
        #Lock picks for this game
        game.pickLocked=True
        game.save()
        print("Locking an upcoming game: " + game.homeTeam.name + " VS " + game.awayTeam.name)
        
    print("The lock picks task ran.")
    return True