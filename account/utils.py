from .models import Profile
from league.models import LeagueMembership
import pytz

def getUserTimezone(user):
    #Get user profile
    userProfile = Profile.objects.get(user=user)
    userTimezone = userProfile.timezone
    return pytz.timezone(userTimezone)

def convertTimeToLocalTimezone(user, dateTimeToConvert):
    tz = getUserTimezone(user)
    localTime = dateTimeToConvert.replace(tzinfo=pytz.utc).astimezone(tz)
    return localTime

def getUserScore(user, league):
    try:
        userScore = LeagueMembership.objects.get(user=user, league=league).score
        return userScore
    except:
        return 0