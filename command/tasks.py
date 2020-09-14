from __future__ import absolute_import, unicode_literals

from celery import shared_task
from league.models import Season, Week, Game, LeagueMembership
from datetime import datetime, timedelta
import pytz

@shared_task
def lockPicks():

    print("Attempting to lock any upcoming games...")
    try:
        #Get current active season
        activeSeason = Season.objects.get(active=True)
    except:
        #Season has not been created, just quit this task
        return True

    #Get all games that are within 15 minutes of start time
    upcomingGames = Game.objects.filter(dateTime__range=[datetime.now(pytz.utc), datetime.now(pytz.utc) + timedelta(minutes=15)])

    for game in upcomingGames:
        #Lock picks for this game which is within a hour from start time
        game.pickLocked=True
        game.save()
        print("Locked an upcoming game: " + game.homeTeam.name + " VS " + game.awayTeam.name)
        
    return True

@shared_task
def saveWeeklyScores():
    try:
        #Get current active season
        activeSeason = Season.objects.get(active=True)
    except:
        #Season has not been created, just quit this task
        return True

    #Get all league membership objects
    allLeagueMemberships = LeagueMembership.objects.all()

    for currentMembership in allLeagueMemberships:
        currentMembership.weeklyScores = currentMembership.weeklyScores + str(currentMembership.score) + ','
        currentMembership.save()

#@shared_task
#def sendReminderEmail():
    