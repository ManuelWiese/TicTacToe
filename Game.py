
class Game:
    def __init__(self):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    # TODO: games with variable number of players?
    @staticmethod
    def getPlayerCount():
        raise NotImplementedError

    def makeTurn(self, move):
        raise NotImplementedError

    def getTurn(self):
        raise NotImplementedError

    def getGameState(self):
        raise NotImplementedError

    def getValidMoves(self):
        raise NotImplementedError

    def getState(self):
        raise NotImplementedError

    def display(self):
        raise NotImplementedError

    def getHeuristics(self, playerNumber):
        raise NotImplementedError
