
class GameLogic:

    def __init__(self):
        raise NotImplementedError

    def makeTurn(self, move):
        raise NotImplementedError

    def getGameState(self):
        raise NotImplementedError

    def getValidMoves(self):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError

    def display(self):
        raise NotImplementedError

    def getHeuristics(self, playerNumber):
        raise NotImplementedError
