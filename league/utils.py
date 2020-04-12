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
        league = None

    return(league)

def getUserActiveLeague(currentUser):
    #Get user profile
    try:
        userProfile = Profile.objects.get(user=currentUser)
    except:
        #All users SHOULD have a profile. Send email to admin if this happens
        print("Could not get profile for user when trying to get active league: " + currentUser.username)
        return None
    
    #Return currentActiveLeague
    return userProfile.currentActiveLeague

def setUserActiveLeague(currentUser, activeLeague):
    #Get user profile
    try:
        userProfile = Profile.objects.get(user=currentUser)
    except:
        #All users SHOULD have a profile. Send email to admin if this happens
        print("Could not get profile for user when trying to set active league: " + currentUser.username)
        return False
    
    #Set activeLeague to the user's current active league
    userProfile.currentActiveLeague = activeLeague
    userProfile.save()

    return True

def getActiveSeason():

    try:
        activeSeason = Season.objects.get(active=True)
    except:
        print("There are currently no active seasons.")
        activeSeason = None
        
    return activeSeason

#Returns string list of week ids for active season
def getWeekIds():
    weekObjects = Week.objects.filter(season=getActiveSeason())
    weeks = []
    for week in weekObjects:
        weeks.append(week.id)
    return weeks