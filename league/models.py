from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class League(models.Model):
    name = models.TextField(max_length=100, blank=True)
    members = models.ManyToManyField(User, through="LeagueMembership")

    def __str__(self):
        return self.name

class Season(models.Model):
    year = models.TextField(max_length=100, blank=True)
    
    def __str__(self):
        return self.year

class Week(models.Model):
    season = models.ForeignKey(Season,on_delete=models.CASCADE, default=None)

class Game(models.Model):
    week = models.ForeignKey(Week,on_delete=models.CASCADE, default=None)
    homeTeam = models.TextField(max_length=50, blank=True)
    awayTeam = models.TextField(max_length=50, blank=True)
    homeCity = models.TextField(max_length=50, blank=True)
    awayCity = models.TextField(max_length=50, blank=True)
    homeScore = models.TextField(max_length=10, blank=True)
    awayScore = models.TextField(max_length=10, blank=True)
    location = models.TextField(max_length=20, blank=True)
    winner = models.TextField(max_length=50, blank=True)
    loser = models.TextField(max_length=50, blank=True)
    users = models.ManyToManyField(User, through="GameChoice")

#This model governs the relationship between a game and a user and who they picked to win the game
class GameChoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    winner = models.TextField(max_length=50, blank=True)
    correctFlag = models.BooleanField(default=False)

#This models governs the relationship between a User and a League they are associated with
class LeagueMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    