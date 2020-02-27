from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class League(models.Model):
    name = models.TextField(max_length=100, blank=True)
    members = models.ManyToManyField(User, through="LeagueMembership")

    def __str__(self):
        return self.name

class Season(models.Model):
    league = models.ForeignKey(League,on_delete=models.CASCADE, default=None)
    year = models.TextField(max_length=100, blank=True)

class Week(models.Model):
    season = models.ForeignKey(Season,on_delete=models.CASCADE, default=None)
    number = models.TextField(max_length=10, blank=True)

class Game(models.Model):
    week = models.ForeignKey(Week,on_delete=models.CASCADE, default=None)
    number = models.TextField(max_length=50, blank=True)
    winner = models.TextField(max_length=50, blank=True)
    loser = models.TextField(max_length=50, blank=True)

#This models governs the relationship between a User and a League they are associated with
class LeagueMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    