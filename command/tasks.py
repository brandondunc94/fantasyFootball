from __future__ import absolute_import, unicode_literals

from celery import shared_task
from league.models import Season, Week, Game, LeagueMembership
from command.utils import sendEmailToUser
from django.contrib.auth.models import User
from django.core import mail

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

    #Get all games that are within 1 minute of start time
    upcomingGames = Game.objects.filter(dateTime__range=[datetime.now(pytz.utc), datetime.now(pytz.utc) + timedelta(minutes=1)])

    for game in upcomingGames:
        #Lock picks for this game which is 1 minute away from start time
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
    allUsers = User.objects.all()
    emailList = [user.email for user in allUsers]

    message = """\
    <html>
        <head>
        </head>
        <body>
            <img src="http://onsidepick.com/static/media/logoTitleWhiteBackground.png" width="250" height="auto">
            <h4>This is a friendly reminder to make your picks and bets for the upcoming week!</h4>
            <a class="btn btn-blue" href="http://onsidepick.com/">Make Picks</a>
            <br><br>
            <p>Want to turn off email notifications? Visit the Account page and remove your email from your profile.</p>
        </body>
    </html>"""


    email = mail.EmailMessage(
                'Make your picks!',
                message,
                'onsidepickfootball@gmail.com',
                [],
                emailList,
                reply_to=['onsidepickfootball@gmail.com'],
                headers={'OnsidePick': 'Reminder'},
        
        )
    email.content_subtype = "html"
    
    
    sendEmailToUser(emailMessages=email, userEmailList=emailList)


