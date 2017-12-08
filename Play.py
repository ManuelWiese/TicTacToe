from Game import Game
import Agent
from InvalidMoveError import InvalidMoveError


class Play:
    def __init__(self, player1, player2):
        assert isinstance(player1, Agent.Agent)
        assert isinstance(player2, Agent.Agent)

        self.player1 = player1
        self.player2 = player2

    def playGame(self):
        game = Game()

        while game.getGameState() == Game.ONGOING:
            if game.getTurn() == 1:
                currentPlayer = self.player1
            else:
                currentPlayer = self.player2

            turn = currentPlayer.makeTurn(game)
            try:
                game.makeTurn(turn)
            except InvalidMoveError:
                currentPlayer.wasInvalidTurn(game, turn)

        return game
