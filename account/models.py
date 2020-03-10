from django.db import models
from django.contrib.auth.models import User
from league.models import League

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentActiveLeague = models.ForeignKey(League, on_delete=models.CASCADE, default="", null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
