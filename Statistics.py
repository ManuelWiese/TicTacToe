from Game import Game


class Statistics:
    def __init__(self):
        self.__ties = 0
        self.__wins = 0
        self.__losses = 0

    def countWin(self):
        self.__wins += 1

    def countLoss(self):
        self.__losses += 1

    def countTie(self):
        self.__ties += 1

    def countGameState(self, gameState, playerNumber):
        if gameState.isTied():
            self.countTie()
        elif gameState.didPlayerWin(playerNumber):
            self.countWin()
        else:
            self.countLoss()

    def getTies(self):
        return self.__ties

    def getLosses(self):
        return self.__losses

    def getWins(self):
        return self.__wins

    def __str__(self):
        output = ("Tied: {}\n".format(self.__ties)
                  + "wins: {}\n".format(self.__wins)
                  + "losses: {}".format(self.__losses))
        return output
