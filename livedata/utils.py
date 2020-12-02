import requests, json
from datetime import date, datetime, timedelta
import league.utils as leagueUtils

def getWeekSchedule():
    weekDates = getWeekDatesList() #Get next 7 days
    weekData = []
    for day in weekDates:
        response = queryApi(querystring={"status":"schedule","league":"NFL","date":day})
        weekData.append(response['results'])

    #Get current active week
    weekId = leagueUtils.getActiveWeekId()
    status = True
    for currentDay in weekData:
        for currentGame in currentDay:
            homeTeamName = currentGame['teams']['home']['mascot'] #Ex. 'Seahawks'
            awayTeamName = currentGame['teams']['away']['mascot']
            try:
                homeSpread = currentGame['odds'][0]['spread']['current']['home'] #Ex. '-7.5'
                awaySpread = currentGame['odds'][0]['spread']['current']['away']
            except:
                homeSpread = ''
                awaySpread = ''
                print('Spread not available for game: ' + currentGame['summary'])
                
            gameDateTime = currentGame['schedule']['date'] #Ex. '2020-09-26T00:07:06.346Z'
            gameDate = gameDateTime[:10] #Ex. '2020-09-26'
            gameTime = gameDateTime[11:-8] #Ex. '00:07'

            #Handle Redskins/ Football Team name change
            if homeTeamName == 'Football Team':
                homeTeamName = 'Redskins'
            
            #def createGame(weekId, homeTeamName, awayTeamName, gameDate, gameTime, homeSpread, awaySpread):
            status = leagueUtils.createGame(weekId=weekId, homeTeamName=homeTeamName,awayTeamName=awayTeamName, gameDate=gameDate, gameTime=gameTime, timezone='', homeSpread=homeSpread, awaySpread=awaySpread)
        
    print('Retrieved schedule for week ' + weekId)
    return status
        
def getInProgressScores():
    
    weekGames = queryApi(querystring={"status":"in progress","league":"NFL","date":(date.today() - timedelta(1)).strftime("%Y-%m-%d") + ',' + date.today().strftime("%Y-%m-%d")})
    print(weekGames)
    status = True
    #Get current active week
    weekId = leagueUtils.getActiveWeekId()
    for currentGame in weekGames['results']:
        try:
            homeTeamName = currentGame['teams']['home']['mascot'] #Ex. 'Seahawks'
            awayTeamName = currentGame['teams']['away']['mascot']

            #Handle Redskins/ Football Team name change
            if homeTeamName == 'Football Team':
                homeTeamName = 'Redskins'
            
            try:
                homeScore = currentGame['scoreboard']['score']['home']
                awayScore = currentGame['scoreboard']['score']['away']
            except:
                homeScore = 0
                awayScore = 0
            try:
                quarter = currentGame['scoreboard']['currentPeriod']
                quarterTimeRemaining = currentGame['scoreboard']['periodTimeRemaining']
            except:
                quarter = '1'
                quarterTimeRemaining = '15:00'

            game = leagueUtils.getGame(homeTeamName=homeTeamName, awayTeamName=awayTeamName, weekId=weekId)
            leagueUtils.updateGame(game=game, homeScore=homeScore, awayScore=awayScore, quarter=quarter, quarterTimeRemaining=quarterTimeRemaining, isComplete=False)
        except:
            status = False
    return status

def getFinalLiveScores():
    weekGames = queryApi(querystring={"status":"final","league":"NFL","date":(date.today() - timedelta(1)).strftime("%Y-%m-%d") + ',' + date.today().strftime("%Y-%m-%d")})

    #Get current active week
    weekId = leagueUtils.getActiveWeekId()
    status = True
    for currentGame in weekGames['results']:
        try:
            homeTeamName = currentGame['teams']['home']['mascot'] #Ex. 'Seahawks'
            awayTeamName = currentGame['teams']['away']['mascot']

            #Handle Redskins/ Football Team name change
            if homeTeamName == 'Football Team':
                homeTeamName = 'Redskins'
            
            homeScore = currentGame['scoreboard']['score']['home']
            awayScore = currentGame['scoreboard']['score']['away']

            try:
                quarter = currentGame['scoreboard']['currentPeriod']
                quarterTimeRemaining = currentGame['scoreboard']['periodTimeRemaining']
            except:
                quarter = 4
                quarterTimeRemaining='00:00'

            game = leagueUtils.getGame(homeTeamName=homeTeamName, awayTeamName=awayTeamName, weekId=weekId)
            leagueUtils.updateGame(game=game, homeScore=homeScore, awayScore=awayScore, quarter=quarter, quarterTimeRemaining=quarterTimeRemaining, isComplete=True)
        except:
            status = False #Failed to either extract data from api response or retrieve/update the game object

    return status

def queryApi(querystring):
    url = "https://sportspage-feeds.p.rapidapi.com/games"

    headers = {
        'x-rapidapi-host': "sportspage-feeds.p.rapidapi.com",
        'x-rapidapi-key': "f3dab5c1f3msh132da6594847d9dp18d4cejsn8983d76c736f"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    weekGames = json.loads(response.text)

    return weekGames
    
def getWeekDatesList(): #Get dates all the way up until the next Sunday
    today = date.today()
    weekdayCounter = today.weekday()
    dayCounter = 1

    weekDates = []
    
    while weekdayCounter != 6:
        weekDates.append((today + timedelta(days=dayCounter)).strftime("%Y-%m-%d"))
        weekdayCounter+=1
        dayCounter+=1

    return weekDates