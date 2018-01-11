from Game import Game
from TicTacToe import TicTacToe
from Agents.Agent import Agent
from InvalidMoveError import InvalidMoveError

from CheckArgs import checkList

import random


class Play:
    def __init__(self, players):
        assert checkList(players, Agent)
        self.players = players

    def playGame(self, shufflePlayers = True):
        if shufflePlayers:
            # TODO: how can we avoid this?
            random.shuffle(self.players)

        game = TicTacToe()

        while game.getGameState().isOngoing():
            if game.getTurn() == game.PLAYER1:
                currentPlayer = self.players[0]
                otherPlayer = self.players[1]
            else:
                currentPlayer = self.players[1]
                otherPlayer = self.players[0]

            try:
                turn = currentPlayer.makeTurn(game)
                game.makeTurn(turn)

                otherPlayer.feedbackAfterOpponentsTurn(game)
            except InvalidMoveError:
                currentPlayer.wasInvalidTurn(game, turn)

        self.players[0].endOfGame(game)
        self.players[1].endOfGame(game)

        return game
