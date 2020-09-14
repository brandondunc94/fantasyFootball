from league.models import Season, Week, Game
from datetime import datetime
from django.core.mail import send_mail

def lockOldGames():
    #Get all game objects older than today's date
    oldGames = Game.objects.filter(dateTime__lte=datetime.utcnow())

    for game in oldGames:
        game.pickLocked = True
        game.save()

    return True

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
    
'''def sendEmailToUser(subject, message):
    try:
        send_mail(
            subject,
            message,
            'brandon.douglas.duncan@gmail.com',
            ['brandon.douglas.duncan@gmail.com'],
            fail_silently=False,
        )
        return True
    except:
        print('Email could not be sent to admin: Subject: ' + subject + ' Message: ' + message)
        return False'''