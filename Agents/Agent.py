
class Agent:
    def __init__(self, playerNumber):
        assert playerNumber == 1 or playerNumber == 2
        self.playerNumber = playerNumber

    def makeTurn(self, game):
        pass

    def feedbackAfterOpponentsTurn(self, game):
        pass

    def wasInvalidTurn(self, game, turn):
        print("Invalid move {}".format(turn))

    def endOfGame(self, game):
        pass
