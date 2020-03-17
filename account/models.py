from django.db import models
from django.contrib.auth.models import User
from league.models import League

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentActiveLeague = models.ForeignKey(League, on_delete=models.CASCADE, default="", null=True)
    firstName = models.TextField(max_length=50, blank=True)
    lastName = models.TextField(max_length=50, blank=True)
