
class Game:
    def __init__(self):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    # TODO: games with variable number of players?
    @staticmethod
    def getPlayerCount():
        raise NotImplementedError

    def makeMove(self, move):
        raise NotImplementedError

    def getTurn(self):
        raise NotImplementedError

    def getGameState(self):
        raise NotImplementedError

    def getValidActions(self):
        raise NotImplementedError

    def getState(self):
        raise NotImplementedError

    def display(self):
        raise NotImplementedError

    def getScore(self, playerNumber):
        raise NotImplementedError
