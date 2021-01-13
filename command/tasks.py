from __future__ import absolute_import, unicode_literals
from celery import shared_task
from league.models import Season, Week, Game, LeagueMembership
from command.utils import sendEmailToUser
from league.utils import getActiveWeek
from django.contrib.auth.models import User
from django.core import mail
from datetime import datetime, timedelta
from livedata.utils import getInProgressScores, getFinalLiveScores
import pytz

@shared_task
def lockPicks():  #This gets run every 5 minutes. Schedule can be found in fantasyFootball/settings.py

    #Get all games that are 1 minute from kickoff time
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
def sendThursdayReminderEmail():  #This gets run every Thursday afternoon. Schedule can be found in fantasyFootball/settings.py
    #Get all user objects and their emails and put into emailList
    allUsers = User.objects.all()
    emailList = [user.email for user in allUsers]

    message = """\
    <html>
    <head>
    </head>
    <style>
    .btn {
        background-color: #19A404;
        border-radius: 5px;
        color: white;
        padding: 10px 10px;
        text-align: center;
        text-decoration: none;
        font-size: 14px;
        }
    </style>
    <body>
        <img src='http://onsidepick.com/static/media/logoTitleWhiteBackground.png' width='250' height='auto'>
        <br><br>
        <h4>Divisonal Playoffs this week. Get your picks and bets in. Point payouts for both picks and bets will be 3x the normal amount!</h4>

        <a class='btn btn-blue' href='http://onsidepick.com/'>Make Picks</a>
        <br><br>
        <p>Don't want email notifications? Please visit the <a href='http://onsidepick.com/account'>Account</a> page and remove the email from your profile.</p>
    </body>
    </html>"""

    #weekId = getActiveWeek().id
    email = mail.EmailMessage(
                'Divisonal Playoffs - Make your picks & earn 3x points!',
                message,
                'onsidepickfootball@gmail.com',
                [],
                emailList,
                reply_to=['onsidepickfootball@gmail.com'],
                headers={'OnsidePick': 'Reminder'},
        
        )
    email.content_subtype = "html"
    
    
    sendEmailToUser(emailMessages=email, userEmailList=emailList)

@shared_task
def sendSundayReminderEmail():  #This gets run every Sunday morning. Schedule can be found in fantasyFootball/settings.py
    #Get all user objects and their emails and put into emailList
    allUsers = User.objects.all()
    emailList = [user.email for user in allUsers]

    message = """\
    <html>
    <head>
    </head>
    <style>
    .btn {
        background-color: #19A404;
        border-radius: 5px;
        color: white;
        padding: 10px 10px;
        text-align: center;
        text-decoration: none;
        font-size: 14px;
        }
    </style>
    <body>
        <img src='http://onsidepick.com/static/media/logoTitleWhiteBackground.png' width='250' height='auto'>
        <br><br>
        <h4>If you haven't yet, this is a friendly reminder to make your picks and bets for today's games!</h4>

        <a class='btn btn-blue' href='http://onsidepick.com/'>Make Picks</a>
        <br><br>
        <p>Don't want email notifications? Please visit the <a href='http://onsidepick.com/account'>Account</a> page and remove the email from your profile.</p>
    </body>
    </html>"""

    weekId = getActiveWeek().id
    email = mail.EmailMessage(
                'Week ' + weekId + ' - Make your Sunday picks!',
                message,
                'onsidepickfootball@gmail.com',
                [],
                emailList,
                reply_to=['onsidepickfootball@gmail.com'],
                headers={'OnsidePick': 'Reminder'},
        
        )
    email.content_subtype = "html"
    
    
    sendEmailToUser(emailMessages=email, userEmailList=emailList)

@shared_task
def getLiveScores():
    try:
        getInProgressScores()
        print('All live scores have been retrieved successfully.')
    except:
        print('Unable to retrieve some live scores.')

@shared_task
def getFinalScores():
    try:
        getFinalLiveScores()
        print('Any final scores have been retrieved successfully.')
    except:
        print('Unable to retrieve/save some final scores.')
