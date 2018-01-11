from Agents.Agent import Agent
from InvalidMoveError import InvalidMoveError

from CheckArgs import checkList

import random


class Play:
    def __init__(self, GameClass, players):
        assert checkList(players, Agent)
        assert len(players) == GameClass.getPlayerCount()

        self.GameClass = GameClass
        self.players = players

    def playGame(self, shufflePlayers = True):
        if shufflePlayers:
            # TODO: how can we avoid this?
            random.shuffle(self.players)

        game = self.GameClass()

        playerIndex = 0

        while game.getGameState().isOngoing():
            currentPlayer = self.players[playerIndex]

            currentPlayer.feedbackBeforeTurn(game)

            try:
                turn = currentPlayer.makeTurn(game)
                game.makeTurn(turn)
                playerIndex = (playerIndex + 1) % len(self.players)

            except InvalidMoveError:
                currentPlayer.wasInvalidTurn(game, turn)


        for player in self.players:
            player.endOfGame(game)

        return game
