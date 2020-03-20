from league.models import League, LeagueMembership, Season, Week, Game
from account.models import Profile
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

#Get all leagues for current user
def getUserLeagues(currentUser):
    leagues = []
    memberships = LeagueMembership.objects.filter(user=currentUser)
    if not memberships:
        return None
    else:
        for currentMembership in memberships:
            leagues.append(currentMembership.league)
        return(leagues)

def getLeague(leagueName):
    try:
        league = League.objects.get(name=leagueName)
    except:
        print("League could not be found: " + leagueName)
        league = None

    return(league)

def getUserActiveLeague(currentUser):
    #Get user profile
    try:
        userProfile = Profile.objects.get(user=currentUser)
    except:
        #All users SHOULD have a profile. Send email to admin if this happens
        print("Could not get profile for user: " + currentUser.username)
        return None
    
    #Return currentActiveLeague
    return userProfile.currentActiveLeague

def setUserActiveLeague(currentUser, activeLeague):
    #Get user profile
    try:
        userProfile = Profile.objects.get(user=currentUser)
    except:
        #All users SHOULD have a profile. Send email to admin if this happens
        print("Could not get profile for user: " + currentUser.username)
        return False
    
    #Set activeLeague to the user's current active league
    userProfile.currentActiveLeague = activeLeague
    userProfile.save()

    return True
    
def updateScores():
    #Update score and winner/loser in DB
    return True

