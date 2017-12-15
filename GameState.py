
class GameState:
    ONGOING, PLAYER1_WON, PLAYER2_WON, TIED = range(4)

    @staticmethod
    def createOngoing():
        return GameState(GameState.ONGOING)

    @staticmethod
    def createPlayer1Won():
        return GameState(GameState.PLAYER1_WON)

    @staticmethod
    def createPlayer2Won():
        return GameState(GameState.PLAYER2_WON)

    @staticmethod
    def createTied():
        return GameState(GameState.TIED)

    def __init__(self, gameState):
        self.gameState = gameState

    def isOngoing(self):
        return self.gameState == GameState.ONGOING

    def isTied(self):
        return self.gameState == GameState.TIED

    def player1Won(self):
        return self.gameState == GameState.PLAYER1_WON

    def player2Won(self):
        return self.gameState == GameState.PLAYER2_WON
