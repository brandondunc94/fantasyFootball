from league.models import League

#Get all leagues for current user
def getUserLeagues(user):
    League = None
    return(League)

def createLeague(user):
    newLeague = League.objects.create(id=1, name="Test League")