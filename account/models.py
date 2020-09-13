from django.db import models
from django.contrib.auth.models import User
from league.models import League

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    currentActiveLeague = models.ForeignKey(League, on_delete=models.CASCADE, default=None, null=True)
    firstName = models.TextField(max_length=50, blank=True)
    lastName = models.TextField(max_length=50, blank=True)
    timezone = models.CharField(max_length=50, blank=True, default="US/Pacific")
    lastPageAccessed = models.TextField(max_length=20, blank=True, default="Home")
