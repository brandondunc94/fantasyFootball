from league.models import League, LeagueMembership, Season, Week, Game
from django.contrib.auth.models import User

#Get all leagues for current user
def getUserLeagues(currentUser):
    leagues = []
    memberships = LeagueMembership.objects.filter(user = currentUser)
    for currentMembership in memberships:
        leagues.append(currentMembership.league)
    return(leagues)

def createNewSeason():
    #Create new season object in db
    newSeason = Season(year=20192020)
    newSeason.save()

    #Create 17 new week objects for new season
    for weekNumber in range(17):
        newWeek = Week(season=newSeason, number = weekNumber)
        newWeek.save()
        #Create 16 game objects per week
        for gameNumber in range(16):
            newGame = Game(week=newWeek, number = gameNumber)
            #Set teams here
            newGame.save()

    



