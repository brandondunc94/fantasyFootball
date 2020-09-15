from league.models import Season, Week, Game, League, LeagueNotification
from league.utils import createLeagueNotification
from datetime import datetime
from django.core.mail import send_mail

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
        newLeagueNotification = LeagueNotification.objects.create(league=currentLeague, message=message)
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
    
def sendEmailToUser(subject, message, userEmailList):
    #try:
    send_mail(
            subject,
            message,
            'onsidepickfootball@gmail.com',
            [userEmailList],
            fail_silently=False,
            html_message=message,
        )
    #print('Email successfully sent to user(s): Subject: ' + subject + ' Message: ' + message)
    return True
    #except:
        #print('Email could not be sent to user(s): Subject: ' + subject + ' Message: ' + message)
        #return False