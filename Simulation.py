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


class Simulation:
    def __init__(self, players):
        assert checkList(players, Agent)
        self.players = players

    def simulate(self, numberOfGames):
        assert isinstance(numberOfGames, int)
        assert numberOfGames >= 0

        play = Play(self.players)

        for i in range(numberOfGames):
            game = play.playGame()
            gameState = game.getGameState()


if __name__ == "__main__":
    player1 = QLearningAgent(0.1, 1, 1.0)
    decision = DecisionTreeAgent()
    monte = MonteCarloAgent(1000)
    human = HumanAgent()
    player2 = MiniMaxAgent(9)

    # simulation = Simulation([player1, player2])
    simulation = Simulation([player1, monte])

    n = 1000
    runs = 100
    for i, epsilon in enumerate([1.0 - k / n for k in range(n + 1)]):

        player1.setEpsilon(epsilon)

        print("Result after {} * {} runs,".format(i + 1, runs)
              + " current epsilon = {}".format(epsilon))

        simulation.simulate(runs)
        print(player1.getStatistics())
        player1.resetStatistics()

    simulation = Simulation([player1, human])
    simulation.simulate(10)
