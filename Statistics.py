
class Statistics:
    def __init__(self):
        self.__tied = 0
        self.__player1Won = 0
        self.__player2Won = 0

    def player1Won(self):
        self.__player1Won += 1

    def player2Won(self):
        self.__player2Won += 1

    def tied(self):
        self.__tied += 1

    def countGameState(self, gameState):
        if gameState.player1Won():
            self.player1Won()
        elif gameState.player2Won():
            self.player2Won()
        else:
            self.tied()

    def getTies(self):
        return self.__tied

    def getLosses(self, playerNumber):
        if playerNumber == 1:
            return self.__player2Won
        return self.__player1Won

    def getWins(self, playerNumber):
        if playerNumber == 1:
            return self.__player1Won
        return self.__player2Won

    def __str__(self):
        output = ("Tied: {}\n".format(self.__tied)
                  + "Player 1 won: {}\n".format(self.__player1Won)
                  + "Player 2 won: {}".format(self.__player2Won))
        return output
