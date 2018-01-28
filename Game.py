
class Game:
    def __init__(self):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    # TODO: games with variable number of players?
    @classmethod
    def getPlayerCount(cls):
        raise NotImplementedError

    def makeMove(self, move):
        raise NotImplementedError

    def getTurn(self):
        raise NotImplementedError

    def getGameStatus(self):
        raise NotImplementedError

    @classmethod
    def getActionSpace(cls):
        raise NotImplementedError

    @classmethod
    def getActionSpaceSize(cls):
        raise NotImplementedError

    def getValidActions(self):
        raise NotImplementedError

    @classmethod
    def getObservationSize(cls):
        raise NotImplementedError

    def getObservation(self):
        raise NotImplementedError

    def getState(self):
        raise NotImplementedError

    def display(self):
        raise NotImplementedError

    def getScore(self, playerNumber):
        raise NotImplementedError
