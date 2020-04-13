from .models import Profile
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