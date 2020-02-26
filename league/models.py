from django.db import models

# Create your models here.
class League(models.Model):
    name = models.TextField(max_length=100, blank=True)

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