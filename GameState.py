
class GameState:

    @staticmethod
    def createOngoing():
        return GameState(True, False, None)

    @staticmethod
    def createPlayerWon(playerNumber):
        return GameState(False, False, playerNumber)

    @staticmethod
    def createTied():
        return GameState(False, True, None)

    def __init__(self, ongoing, tied, winner):
        self.ongoing = ongoing
        self.tied = tied
        self.winner = winner

    def isOngoing(self):
        return self.ongoing

    def isTied(self):
        return self.tied

    def getWinner(self):
        return self.winner

    def didPlayerWin(self, playerNumber):
        return self.winner == playerNumber
