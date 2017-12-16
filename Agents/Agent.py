
class Agent:
    def __init__(self):
        self.playerNumber = None

    def makeTurn(self, game):
        self.playerNumber = game.getTurn()

    def feedbackAfterOpponentsTurn(self, game):
        pass

    def wasInvalidTurn(self, game, turn):
        print("Invalid move {}".format(turn))

    def endOfGame(self, game):
        pass
