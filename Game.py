from InvalidMoveError import InvalidMoveError

from GameLogic import GameLogic


class Game:
    PLAYER1 = 1
    PLAYER2 = 2

    def __init__(self, gameLogic):
        assert isinstance(gameLogic, GameLogic)

        self.gameLogic = gameLogic
        self.turn = Game.PLAYER1

    def copy(self):
        newGame = Game(self.gameLogic.copy())
        newGame.turn = self.turn

        return newGame

    def makeTurn(self, move):
        if move not in self.gameLogic.getValidMoves():
            raise InvalidMoveError()

        self.gameLogic.makeTurn(move, self.turn)

        if self.turn == Game.PLAYER1:
            self.turn = Game.PLAYER2
        else:
            self.turn = Game.PLAYER1

    def getTurn(self):
        return self.turn

    def getFirstTurn(self):
        return self.firstTurn

    def getGameState(self):
        return self.gameLogic.getGameState()

    def getValidMoves(self):
        return self.gameLogic.getValidMoves()

    def getState(self):
        return hash(self.gameLogic)

    def display(self):
        self.gameLogic.display()

    def getHeuristics(self, playerNumber):
        assert playerNumber == Game.PLAYER1 or playerNumber == Game.PLAYER2
        return self.gameLogic.getHeuristics(playerNumber)
