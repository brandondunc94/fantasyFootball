from league.models import Season, Week, Game, League, LeagueNotification
from league.utils import createLeagueNotification
from datetime import datetime
from django.core import mail

def lockOldGames():
    #Get all game objects older than today's date
    oldGames = Game.objects.filter(dateTime__lte=datetime.utcnow())

    for game in oldGames:
        game.pickLocked = True
        game.save()

    return True

def logSystemNotification():
    #Get all leagues
    allLeagues = League.objects.all()

    message = input("Enter league message: ") 
    for currentLeague in allLeagues:
        #Create leagueNotification for current league
        newLeagueNotification = LeagueNotification.objects.create(league=currentLeague, message=message, notificationType='SYS')
        newLeagueNotification.save()

def sendEmailToAdmin(subject, message):
    try:
        send_mail(
            subject,
            message,
            'onsidepickfootball@gmail.com',
            ['brandon.douglas.duncan@gmail.com'], #Admin email goes here
            fail_silently=False,
        )
        return True
    except:
        print('Email could not be sent to admin: Subject: ' + subject + ' Message: ' + message)
        return False
    
def sendEmailToUser(emailMessages, userEmailList):
    try:
        connection = mail.get_connection()
        connection.send_messages([emailMessages])

        print('Email successfully sent to user(s).')
        return True
    except:
        print('Email could not be sent to user(s).')
        return False