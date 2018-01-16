import random
from Play import Play

from Agents.Agent import Agent
from Agents.RandomAgent import RandomAgent
from Agents.DecisionTreeAgent import DecisionTreeAgent
from Agents.HumanAgent import HumanAgent
from Agents.MonteCarloAgent import MonteCarloAgent
from Agents.MiniMaxAgent import MiniMaxAgent
from Agents.QLearningAgent import QLearningAgent

from Statistics import Statistics

from CheckArgs import checkList

from Game import Game
from TicTacToe import TicTacToe


class Simulation:
    def __init__(self, GameClass, players):
        assert checkList(players, Agent)
        assert Game in GameClass.__bases__
        assert len(players) == GameClass.getPlayerCount()
        self.GameClass = GameClass
        self.players = players


    def simulate(self, numberOfGames):
        assert isinstance(numberOfGames, int)
        assert numberOfGames >= 0

        play = Play(self.GameClass, self.players)

        for i in range(numberOfGames):
            game = play.playGame()


if __name__ == "__main__":
    players = [QLearningAgent(0.1, 1, 1.0), MonteCarloAgent(1000)]

    simulation = Simulation(TicTacToe, players)

    n = 1000
    runs = 1000
    for i, epsilon in enumerate([1.0 - k / n for k in range(n + 1)]):

        players[0].setEpsilon(epsilon)

        print("Result after {} * {} runs,".format(i + 1, runs)
              + " current epsilon = {}".format(epsilon))

        simulation.simulate(runs)
        print(players[0].getStatistics())
        players[0].resetStatistics()
