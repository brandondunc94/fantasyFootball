from league.models import Season, Week, Game
from datetime import datetime

def lockOldGames():
    #Get all game objects older than today's date
    oldGames = Game.objects.filter(dateTime__lte=datetime.utcnow())

    for game in oldGames:
        game.pickLocked = True
        game.save()

    return True