from Statistics import Statistics
from Game import Game

class Agent:
    def __init__(self):
        self.playerNumber = None
        self.statistics = Statistics()

    def getAction(self, game):
        self.playerNumber = game.getTurn()

    def feedbackBeforeTurn(self, game):
        pass

    def wasInvalidTurn(self, game, turn):
        print("Invalid move {}".format(turn))

    def endOfGame(self, game):
        self.statistics.countGameState(game.getGameStatus(), self.playerNumber)

    def resetStatistics(self):
        self.statistics = Statistics()

    def getStatistics(self):
        return self.statistics
