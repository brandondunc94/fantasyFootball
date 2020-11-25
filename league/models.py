from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class League(models.Model):
    name = models.TextField(primary_key=True, max_length=100, blank=True)
    members = models.ManyToManyField(User, through="LeagueMembership")
    description = models.TextField(max_length=100, default="")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin", default="", null=True)
    isPublic = models.BooleanField(default="False")
    class Meta:
        unique_together = ["name"]

    def __str__(self):
        return self.name
    

class Season(models.Model):
    year = models.TextField(primary_key=True, max_length=100, blank=True)
    active = models.BooleanField(default=True)
    currentActiveWeek = models.TextField(max_length=100, default="1")
    
    def __str__(self):
        return self.year

class Week(models.Model):
    season = models.ForeignKey(Season,on_delete=models.CASCADE, default=2020)
    weekId = models.IntegerField(default=0)
    altName = models.TextField(max_length=100, default="Regular Season")
    isLocked = models.BooleanField(default=True)

class Team(models.Model):
    name = models.TextField(primary_key=True, max_length=50, blank=True)
    city = models.TextField(max_length=50, blank=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    season = models.ForeignKey(Season,on_delete=models.CASCADE, default=2020)

class Game(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE, default=None)
    homeTeam = models.ForeignKey(Team, on_delete=models.SET_NULL, default=None, null=True, related_name="home")
    awayTeam = models.ForeignKey(Team, on_delete=models.SET_NULL, default=None, null=True, related_name="away")
    season = models.ForeignKey(Season,on_delete=models.CASCADE, null=True, default=2020)
    homeScore = models.IntegerField(default=0)
    awayScore = models.IntegerField(default=0)
    location = models.TextField(max_length=20, blank=True)
    dateTime = models.DateTimeField(auto_now=False, null=True)
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, default=None, null=True, related_name="winner")
    loser = models.ForeignKey(Team, on_delete=models.SET_NULL, default=None, null=True, related_name="loser")
    spreadWinner = models.ForeignKey(Team, on_delete=models.SET_NULL, default=None, null=True, related_name="spreadwinner")
    homeSpread = models.FloatField(default=0)
    awaySpread = models.FloatField(default=0)
    users = models.ManyToManyField(User, through="GameChoice")
    pickLocked = models.BooleanField(default=False)
    isComplete = models.BooleanField(default=False)
    quarter = models.TextField(max_length=5, default='1')
    timeRemaining = models.TextField(max_length=10, default='15:00')

#This model governs the relationship between a game and a user and who they picked/betted on to win the game
class GameChoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    season = models.ForeignKey(Season,on_delete=models.CASCADE, null=True, default=2020)
    pickWinner = models.ForeignKey(Team, on_delete=models.SET_NULL, default=None, null=True,  related_name="pickWinner")
    betWinner = models.ForeignKey(Team, on_delete=models.SET_NULL, default=None, null=True, related_name="betWinner")
    betAmount = models.IntegerField(default=0)
    amountWon = models.IntegerField(default=0)
    correctPickFlag = models.BooleanField(default=None,null=True)
    correctBetFlag = models.BooleanField(default=None,null=True)
    scoredFlag = models.BooleanField(default=None,null=True)

#This models governs the relationship between a User and a League they are associated with
class LeagueMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    season = models.ForeignKey(Season,on_delete=models.CASCADE, null=True, default='2020')
    score = models.IntegerField(default=500)
    correctPicks = models.IntegerField(default=0)
    correctBets = models.IntegerField(default=0)
    weeklyScores = models.TextField(max_length=1000, blank=True, default="") #Comma separated list of weekly scores starting with week 1
    class Meta:
        unique_together = ["user", "league"]

class LeagueMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    message = models.TextField(max_length=500, blank=True)
    createDate = models.DateTimeField(auto_now=True)

class LeagueNotification(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    message = models.TextField(max_length=500, blank=True)
    createDate = models.DateTimeField(auto_now=True)
    SCORE = 'SCR'
    SYSTEM = 'SYS'
    NOTIFICATION_TYPES = [
        (SCORE, 'Score'),
        (SYSTEM, 'System'),
    ]
    notificationType = models.CharField(
        max_length=3,
        choices=NOTIFICATION_TYPES,
        default=SCORE,
    )

class LeagueMembershipRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    requestDate = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ["user", "league"]