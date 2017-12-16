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


class Simulation:
    def __init__(self, player1, player2):
        assert isinstance(player1, Agent)
        assert isinstance(player2, Agent)

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
    player1 = QLearningAgent(0.1, 1, 1.0)
    player2 = RandomAgent()

    simulation = Simulation(player1, player2)

    n = 1000
    runs = 100
    for i, epsilon in enumerate([1.0 - k / n for k in range(n + 1)]):

        player1.setEpsilon(epsilon)

        print("Result after {} * {} runs,".format(i + 1, runs)
              + " current epsilon = {}".format(epsilon))

        print(simulation.simulate(runs))

    simulation = Simulation(player1, player2)
    print(simulation.simulate(10000))
    simulation = Simulation(MiniMaxAgent(9), RandomAgent())
    print(simulation.simulate(10000))
