from django.db import models
from django.contrib.auth.models import User
from league.models import League, Season, Week, Game

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    league = models.ForeignKey(League,on_delete=models.CASCADE, default=None)

