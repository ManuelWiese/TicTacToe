import random
from Play import Play
from Game import Game

from Agents.RandomAgent import RandomAgent
from Agents.DecisionTreeAgent import DecisionTreeAgent
from Agents.BruteForceAgent import *
from Agents.HumanAgent import HumanAgent
from Agents.MonteCarloAgent import MonteCarloAgent
from Agents.MiniMaxAgent import MiniMaxAgent
from Agents.QLearningAgent import QLearningAgent

from Statistics import Statistics


class Simulation:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def simulate(self, numberOfGames):
        assert isinstance(numberOfGames, int)
        assert numberOfGames >= 0

        play = Play(self.player1, self.player2)
        statistics = Statistics()

        for i in range(numberOfGames):
            game = play.playGame(firstTurn=random.choice([1, 2]))
            gameState = game.getGameState()

            statistics.countGameState(gameState)

        return statistics

if __name__ == "__main__":
    player1 = QLearningAgent(1, 0.5, 1, 1.0)
    player2 = RandomAgent(2)

    simulation = Simulation(player1, player2)

    n = 200
    runs = 1000
    for i, epsilon in enumerate([1.0 - k / n for k in range(n + 1)]):

        player1.setEpsilon(epsilon)

        print("Result after {} * {} runs, current epsilon = {}".format(i + 1, runs, epsilon))
        print(simulation.simulate(runs))

    player2 = QLearningAgent(2, 0.1, 1, 0.0)

    simulation = Simulation(player1, player2)
    print(simulation.simulate(10000))
