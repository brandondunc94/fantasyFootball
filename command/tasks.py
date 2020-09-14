from __future__ import absolute_import, unicode_literals

from celery import shared_task
from league.models import Season, Week, Game, LeagueMembership
from command.utils import sendEmailToUser
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import pytz

@shared_task
def lockPicks():  #This gets run every 5 minutes. Schedule can be found in fantasyFootball/settings.py

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
def saveWeeklyScores(): #This gets run every Tuesday morning. Schedule can be found in fantasyFootball/settings.py
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

@shared_task
def sendReminderEmail():  #This gets run every Thursday afternoon. Schedule can be found in fantasyFootball/settings.py
    #Get all user objects and their emails and put into emailList
    #allUsers = User.objects.all()
    allUsers = User.objects.get(username='bdunc')
    
    #emailList = [user.email for user in allUsers]
    emailList = [allUsers.email]
    message = """\
    <html>
        <head>ONSIDEPICK</head>
        <body>
            <p>Be sure to make your picks!
            <br>
                Here is the <a href="https://www.python.org">link</a> you wanted.
            </p>
        </body>
    </html>"""

    sendEmailToUser(subject='OnsidePick - Make your picks', message=message, userEmailList=emailList)