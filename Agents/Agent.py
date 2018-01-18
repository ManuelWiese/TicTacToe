from Statistics import Statistics


class Agent:
    def __init__(self, collectStatistics=True):
        self.playerNumber = None
        self.collectStatistics = collectStatistics
        if self.collectStatistics:
            self.statistics = Statistics()
        else:
            self.statistics = None

    def getAction(self, game):
        self.playerNumber = game.getTurn()

    def feedbackBeforeTurn(self, game):
        pass

    def wasInvalidAction(self, game, turn):
        print("Invalid move {}".format(turn))

    def endOfGame(self, game):
        if self.collectStatistics:
            self.statistics.countGameState(game.getGameStatus(), self.playerNumber)

    def resetStatistics(self):
        if self.statistics is not None:
            self.statistics = Statistics()

    def setCollectStatistics(self, collectStatistics):
        self.collectStatistics = collectStatistics
        if self.statistics is None:
            self.statistics = Statistics()

    def getStatistics(self):
        return self.statistics
