from league.models import League, LeagueMembership, Season, Week, Game
from django.contrib.auth.models import User
import json

#Get all leagues for current user
def getUserLeagues(currentUser):
    leagues = []
    memberships = LeagueMembership.objects.filter(user = currentUser)
    for currentMembership in memberships:
        leagues.append(currentMembership.league)
    return(leagues)

    
def updateScores():
    #Update score and winner/loser in DB
    return True


