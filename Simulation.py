import random

from InvalidMoveError import InvalidMoveError

from Agents.Agent import Agent
from Agents.RandomAgent import RandomAgent
from Agents.DecisionTreeAgent import DecisionTreeAgent
from Agents.HumanAgent import HumanAgent
from Agents.MonteCarloAgent import MonteCarloAgent
from Agents.MiniMaxAgent import MiniMaxAgent
from Agents.QLearningAgent import QLearningAgent


from CheckArgs import checkList

from Game import Game
from TicTacToe import TicTacToe
import copy


class Simulation:
    def __init__(self, GameClass, players):
        assert checkList(players, Agent)
        assert Game in GameClass.__bases__
        assert len(players) == GameClass.getPlayerCount()
        self.GameClass = GameClass
        self.players = copy.copy(players)

    def playGame(self, shufflePlayers = True):
        if shufflePlayers:
            random.shuffle(self.players)

        game = self.GameClass()

        while game.getGameStatus().isOngoing():
            currentPlayer = self.players[game.getTurn()]

            currentPlayer.feedbackBeforeTurn(game)

            action = currentPlayer.getAction(game)
            try:
                game.makeMove(action)

            except InvalidMoveError:
                currentPlayer.wasInvalidAction(game, action)

        for player in self.players:
            player.endOfGame(game)

        return game

    def simulate(self, numberOfGames):
        assert isinstance(numberOfGames, int)
        assert numberOfGames >= 0

        for i in range(numberOfGames):
            self.playGame()


if __name__ == "__main__":
    from Agents.QLearningAgent import QFunction

    q = QFunction()

    players = [QLearningAgent(1.0, 1.0, 1.0, qfunction=q), QLearningAgent(1.0, 1.0, 1.0, qfunction=q)]

    simulation = Simulation(TicTacToe, players)

    n = 1000
    runs = 1000
    for i, epsilon in enumerate([1.0 - k / n for k in range(n + 1)]):

        players[0].setEpsilon(epsilon)
        players[1].setEpsilon(epsilon)

        print("Result after {} * {} runs,".format(i + 1, runs)
              + " current epsilon = {}".format(epsilon))

        simulation.simulate(runs)
        print(players[0].getStatistics())
        players[0].resetStatistics()

    players[1] = MonteCarloAgent(1000)

    simulation.simulate(runs)
    print(players[0].getStatistics())