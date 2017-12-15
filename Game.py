from InvalidMoveError import InvalidMoveError

from CheckArgs import checkIntBetween
from CheckArgs import checkTuple

from GameState import GameState
from GameLogic import GameLogic

import copy

class Game:

    def __init__(self, gameLogic, firstTurn=1):
        assert isinstance(gameLogic, GameLogic)
        assert isinstance(firstTurn, int)

        self.gameLogic = gameLogic
        self.firstTurn = firstTurn
        self.turn = self.firstTurn

    def copy(self):
        newGame = Game(copy.deepcopy(self.gameLogic), self.firstTurn)
        newGame.turn = self.turn

        return newGame

    def makeTurn(self, move):
        if not move in self.gameLogic.getValidMoves():
            raise InvalidMoveError()

        self.gameLogic.makeTurn(move, self.turn)

        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

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
        assert playerNumber == 1 or playerNumber == 2
        return self.gameLogic.getHeuristics(playerNumber)
