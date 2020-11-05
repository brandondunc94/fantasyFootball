from django.contrib.auth.models import User
from league.models import League, LeagueMembership, Season, Week, Game, GameChoice

def calculatePlayerCorrectPicks():

    allLeagueMemberships = LeagueMembership.objects.all()

    for currentMembership in allLeagueMemberships:
        #Get all game choices for current user and league where correctPickFlag == True
        currentMembership.correctPicks = GameChoice.objects.filter(user=currentMembership.user, league=currentMembership.league, correctPickFlag=True).count()
        currentMembership.save()


