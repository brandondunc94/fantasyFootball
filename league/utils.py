from league.models import League, LeagueMembership, Season, Week, Game, LeagueNotification, Team, GameChoice
from account.models import Profile
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime
import json, pytz

#Get all leagues for current user
def getUserLeagues(currentUser):
    leagues = []
    memberships = LeagueMembership.objects.filter(user=currentUser)
    if not memberships:
        return None
    else:
        for currentMembership in memberships:
            leagues.append(currentMembership.league)
        return(leagues)

def getLeague(leagueName):
    try:
        league = League.objects.get(name=leagueName)
    except:
        league = None

    return(league)

def getUserActiveLeague(currentUser):
    #Get user profile
    try:
        userProfile = Profile.objects.get(user=currentUser)
    except:
        #All users SHOULD have a profile. Send email to admin if this happens
        print("Could not get profile for user when trying to get active league: " + currentUser.username)
        return None
    
    #Return currentActiveLeague
    return userProfile.currentActiveLeague

def setUserActiveLeague(currentUser, activeLeague):
    #Get user profile
    try:
        userProfile = Profile.objects.get(user=currentUser)
    except:
        #All users SHOULD have a profile. Send email to admin if this happens
        print("Could not get profile for user when trying to set active league: " + currentUser.username)
        return False
    
    #Set activeLeague to the user's current active league
    userProfile.currentActiveLeague = activeLeague
    userProfile.save()

    return True

def getActiveSeason():

    try:
        activeSeason = Season.objects.get(active=True)
    except:
        print("There are currently no active seasons.")
        activeSeason = None
        
    return activeSeason

def getActiveWeekId():
    try:
        activeWeekId = getActiveSeason().currentActiveWeek
    except:
        activeWeekId = 0
    
    return activeWeekId
    
#Returns string list of week ids for active season
def getWeekIds():
    weekObjects = Week.objects.filter(season=getActiveSeason())
    weeks = []
    for week in weekObjects:
        weeks.append(week.id)
    return weeks

#Post new update to league updates
def createLeagueNotification(leagueName, message):
    try:
        league = League.objects.get(name=leagueName)
        newLeagueNotification = LeagueNotification.objects.create(league=league, message=message)
        newLeagueNotification.save()
    except:
        print("Could not post league update.")
    
    return

#Get game object
def getGame(homeTeamName, awayTeamName, weekId):
    try:
        homeTeam = Team.objects.get(name=homeTeamName)
        awayTeam = Team.objects.get(name=awayTeamName)
        week = Week.objects.get(id=weekId)
        game = Game.objects.get(homeTeam=homeTeam, awayTeam=awayTeam, week=week)
    except:
        game = None
    
    return game

#Create new game
def createGame(weekId, homeTeamName, awayTeamName, gameDate, gameTime, timezone, homeSpread, awaySpread):
    
    try:
        #Get active season and week object
        season = getActiveSeason()
        week = Week.objects.get(id=weekId, season=season)

        #If week is locked, don't add the game
        if week.isLocked:
            print("Week is locked, unable to create new game.")
            status = False
            return status

        #Get team objects
        homeTeam = Team.objects.get(name=homeTeamName)
        awayTeam = Team.objects.get(name=awayTeamName)

        gameDateTimeObject = convertGameDateTimeToDB(gameDate=gameDate, gameTime=gameTime, timezone=timezone)
        
        try:
            homeSpread = float(homeSpread)
            awaySpread = float(awaySpread)
        except:
            homeSpread = 0
            awaySpread = 0

        #Search for existing game
        try:
            existingGame = Game.objects.get(homeTeam=homeTeam, awayTeam=awayTeam, week=week)
            #This will be before the game has started so we only need to update the spreads and game date/time
            print("Game already exists, updating game instead.")
            updateGame(game=existingGame, homeSpread=homeSpread, awaySpread=awaySpread, gameDate=gameDate, gameTime=gameTime, isComplete=False)
        except:
            #Create the new game
            newGame = Game(week=week, homeTeam=homeTeam, awayTeam=awayTeam, dateTime=gameDateTimeObject, homeSpread=homeSpread, awaySpread=awaySpread) #Create game
            newGame.save()
        status = True
    except:
        print("Unable to create new game.")
        status = False

    return status

#Update existing game - Necessary values to be passed in are game and isComplete
def updateGame(game, homeSpread='', awaySpread='', gameDate='', gameTime='', timezone='', homeScore='', awayScore='', quarter='', quarterTimeRemaining='', isComplete=False):
    try:
        #If week is locked or game is complete, don't do anything
        if game.week.isLocked or game.isComplete:
            return

        #Update spreads
        if homeSpread != '' and awaySpread != '':
            try:
                game.homeSpread = float(homeSpread)
                game.awaySpread = float(awaySpread)
            except:
                game.homeSpread = 0
                game.awaySpread = 0

        #Update game date/time
        if gameDate != '' and gameTime != '':
            game.dateTime = convertGameDateTimeToDB(gameDate=gameDate, gameTime=gameTime, timezone=timezone)

        #Update scores
        if homeScore != '' and awayScore != '':
            try:
                game.homeScore = int(homeScore)
                game.awayScore = int(awayScore)
            except:
                game.homeScore = 0
                game.awayScore = 0

        #If game is complete, set winner/loser & score players
        if isComplete:
            game.isComplete = True
            determineWinner(game)
            scoreGame(game=game) #*THIS WOULD BE A GOOD TASK FOR A TASK QUEUE*
        else:
            #Update in progress game quarter/time remaining
            if quarter != '' and quarterTimeRemaining != '':
                game.quarter = quarter
                game.timeRemaining = quarterTimeRemaining
        
        game.save() #Save game updates to DB
    except:
        print('Could not update game.')

    return

#Set winner/loser of game and set wins/losses/ties
def determineWinner(game):
    if (game.homeScore > game.awayScore):
        game.winner = game.homeTeam
        game.homeTeam.wins += 1
        game.awayTeam.losses += 1
    elif (game.awayScore > game.homeScore):
        game.winner = game.awayTeam
        game.homeTeam.losses += 1
        game.awayTeam.wins += 1
    else:
        game.winner = None
        game.homeTeam.ties += 1
        game.awayTeam.ties += 1
    
    #Save home and away wins/losses update, save team changes
    game.homeTeam.save()
    game.awayTeam.save()

#Score all players on the game passed in
def scoreGame(game):

    #Update user scores
    allUsers = User.objects.all()   #Get all users

    for currentUser in allUsers:
        #Get game choices for current game and current user (1 per league that the user is in)
        picks = GameChoice.objects.filter(user=currentUser, game=game)
        
        for currentPick in picks:
            membership = LeagueMembership.objects.get(user=currentUser, league=currentPick.league)
            
            if currentPick.scoredFlag == None: #This game choice has not yet been scored
                currentPick.scoredFlag = True #Mark this game as scored
                #Give player 25 points if they got this game correct 
                if currentPick.pickWinner == game.winner:
                    membership.score += 25
                    currentPick.correctPickFlag = True

                #Check if spread bet was correct and give points accordingly
                if currentPick.betWinner:
                    if currentPick.betWinner == game.homeTeam: #User selected home team spread
                        if game.homeSpread < game.awaySpread: #Home Team was supposed to win
                            if game.homeScore - game.awayScore >= game.awaySpread: #Home team won by their spread, pay player
                                currentPick.amountWon += currentPick.betAmount * .9
                                membership.score += currentPick.amountWon
                                currentPick.correctBetFlag = True
                            else:   #Home team did not win by their spread, take player's points
                                currentPick.amountWon -= currentPick.betAmount
                                membership.score += currentPick.amountWon #This will be negative
                                currentPick.correctBetFlag = False
                        elif game.awaySpread < game.homeSpread: #Home team was supposed to lose
                            if game.awayScore - game.homeScore <= game.homeSpread: #Home team lost within their spread margin or won, pay player
                                currentPick.amountWon += currentPick.betAmount * .9
                                membership.score += currentPick.amountWon
                                currentPick.correctBetFlag = True
                            else:   #Home team lost by too many points, take player's points
                                currentPick.amountWon -= currentPick.betAmount
                                membership.score += currentPick.amountWon #This will be negative
                                currentPick.correctBetFlag = False
                    else: #User selected away team spread
                        if game.awaySpread < game.homeSpread: #Away Team was supposed to win
                            if game.awayScore - game.homeScore >= game.homeSpread: #Away team won by their spread, pay player
                                currentPick.amountWon += currentPick.betAmount * .9
                                membership.score += currentPick.amountWon
                                currentPick.correctBetFlag = True
                            else:   #Away team did not win by their spread, take player's points
                                currentPick.amountWon -= currentPick.betAmount
                                membership.score += currentPick.amountWon #This will be negative
                                currentPick.correctBetFlag = False
                        elif game.homeSpread < game.awaySpread: #Away team was supposed to lose
                            if game.homeScore - game.awayScore <= game.awaySpread: #Away team lost within their spread margin or won, pay player
                                currentPick.amountWon += currentPick.betAmount * .9
                                membership.score += currentPick.amountWon
                                currentPick.correctBetFlag = True
                            else:   #Away team lost by too many points, take player's points
                                currentPick.amountWon -= currentPick.betAmount
                                membership.score += currentPick.amountWon #This will be negative
                                currentPick.correctBetFlag = False
                    if currentPick.amountWon > 100:
                        #Player scored a boat load of points, create a league notification about it
                        message = 'Score Update - ' + currentUser.username + " scored " + str(int(currentPick.amountWon)) + " points by betting on the " + currentPick.betWinner.name + "!"
                        createLeagueNotification(currentPick.league.name, message)
                        
            membership.save()
            currentPick.save()

def convertGameDateTimeToDB(gameDate, gameTime, timezone):
    #Convert gameDateTime to a datetime object in format yyyy-MM-dd HH:mm
    gameDateTimeString = gameDate + " " + gameTime
    gameDateTime = datetime.strptime(gameDateTimeString,'%Y-%m-%d %H:%M')

    #If timezone was passed in, add it to the datetime object
    if timezone != '':
        timezoneObject = pytz.timezone(timezone)
        gameDateTime = timezoneObject.localize(gameDateTime)
        gameDateTime = gameDateTime.astimezone(pytz.utc) #Convert to utc before storing in database
    else: #No timezone passed in - assume time is already in utc, et timezone
        gameDateTime = gameDateTime.replace(tzinfo=pytz.UTC)
    return gameDateTime