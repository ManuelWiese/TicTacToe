from Agents.Agent import Agent
from InvalidMoveError import InvalidMoveError

from CheckArgs import checkList

import random
import copy


class Play:
    def __init__(self, GameClass, players):
        assert checkList(players, Agent)
        assert len(players) == GameClass.getPlayerCount()

        self.GameClass = GameClass
        self.players = copy.copy(players)

    def playGame(self, shufflePlayers = True):
        if shufflePlayers:
            # TODO: how can we avoid this?
            random.shuffle(self.players)

        game = self.GameClass()

        while game.getGameState().isOngoing():
            currentPlayer = self.players[game.getTurn()]

            currentPlayer.feedbackBeforeTurn(game)

            try:
                action = currentPlayer.getAction(game)
                game.makeMove(action)

            except InvalidMoveError:
                currentPlayer.wasInvalidTurn(game, action)

        for player in self.players:
            player.endOfGame(game)

        return game
