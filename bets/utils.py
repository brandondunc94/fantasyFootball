from league.models import LeagueMembership, GameChoice
from league.utils import getActiveSeason

def determineCorrectBetFlag(game, gameChoice):
    if gameChoice:
        if gameChoice.betWinner:
            if gameChoice.betWinner == game.homeTeam: #User selected home team spread
                if game.homeSpread < game.awaySpread: #Home Team was supposed to win
                    if game.homeScore - game.awayScore >= game.awaySpread: #Home team won by their spread, pay player
                        correctBetFlag = True
                    else:   #Home team did not win by their spread, take player's points
                        correctBetFlag = False
                elif game.awaySpread < game.homeSpread: #Home team was supposed to lose
                    if game.awayScore - game.homeScore <= game.homeSpread: #Home team lost within their spread margin or won, pay player
                        correctBetFlag = True
                    else:   #Home team lost by too many points, take player's points
                        correctBetFlag = False
                else: #Spreads are 0/0, check if home team is winning or not
                    if game.homeScore > game.awayScore:
                        correctBetFlag = True
                    else:
                        correctBetFlag = False
            else: #User selected away team spread
                if game.awaySpread < game.homeSpread: #Away Team was supposed to win
                    if game.awayScore - game.homeScore >= game.homeSpread: #Away team won by their spread, pay player
                        correctBetFlag = True
                    else:   #Away team did not win by their spread, take player's points
                        correctBetFlag = False
                elif game.homeSpread < game.awaySpread: #Away team was supposed to lose
                    if game.homeScore - game.awayScore <= game.awaySpread: #Away team lost within their spread margin or won, pay player
                        correctBetFlag = True
                    else:   #Away team lost by too many points, take player's points
                        correctBetFlag = False
                else: #Spreads are 0/0, check if away team is winning or not
                    if game.awayScore > game.homeScore:
                        correctBetFlag = True
                    else:
                        correctBetFlag = False
        else: 
            correctBetFlag = False
    else:
        correctBetFlag = False
        
    return correctBetFlag

def calculatePlayerCorrectBets():

    allLeagueMemberships = LeagueMembership.objects.all()
    activeSeason = getActiveSeason()
    for currentMembership in allLeagueMemberships:
        #Get all game choices for current user and league where correctPickFlag == True
        currentMembership.correctBets = GameChoice.objects.filter(user=currentMembership.user, league=currentMembership.league, correctBetFlag=True, season=activeSeason).count()
        currentMembership.save()