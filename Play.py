from Game import Game
from Game import TicTacToe
import Agent
from InvalidMoveError import InvalidMoveError


class Play:
    def __init__(self, player1, player2):
        assert isinstance(player1, Agent.Agent)
        assert isinstance(player2, Agent.Agent)

        self.player1 = player1
        self.player2 = player2

    def playGame(self, firstTurn=1):
        assert firstTurn == 1 or firstTurn == 2
        game = Game(TicTacToe(), firstTurn)

        while game.getGameState().isOngoing():
            if game.getTurn() == 1:
                currentPlayer = self.player1
            else:
                currentPlayer = self.player2

            turn = currentPlayer.makeTurn(game)
            try:
                game.makeTurn(turn)
            except:
                currentPlayer.wasInvalidTurn(game, turn)

        self.player1.endOfGame(game)
        self.player2.endOfGame(game)

        return game
