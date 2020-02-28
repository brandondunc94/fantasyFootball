from league.models import League, LeagueMembership
from django.contrib.auth.models import User

#Get all leagues for current user
def getUserLeagues(currentUser):
    leagues = []
    memberships = LeagueMembership.objects.filter(user = currentUser)
    for currentMembership in memberships:
        leagues.append(currentMembership.league)
    return(leagues)
