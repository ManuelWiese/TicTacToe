import random
from Play import Play
from Game import Game
import Agent


class Statistics:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def simulate(self, numberOfGames):
        assert isinstance(numberOfGames, int)
        assert numberOfGames >= 0

        play = Play(self.player1, self.player2)
        finalGameStates = [0, 0, 0, 0, 0]

        for i in range(numberOfGames):
            game = play.playGame(random.choice([1, 2]))
            finalGameStates[game.getGameState()] += 1

        return finalGameStates

if __name__ == "__main__":
    player1 = Agent.RandomAgent(1)
    player2 = Agent.DecisionTreeAgent(2)

    statistics = Statistics(player1, player2)

    print(statistics.simulate(100))
