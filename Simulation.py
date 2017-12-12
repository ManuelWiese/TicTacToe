import random
from Play import Play
from Game import Game
import Agent
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
    player1 = Agent.DecisionTreeAgent(1)
    player2 = Agent.RandomAgent(2)

    simulation = Simulation(player1, player2)

    print(simulation.simulate(100))
