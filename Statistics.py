import random
from Play import Play
from Game import Game
import Agent


class Statistics:
    def __init__(self):
        self.__tied = 0
        self.__player1Won = 0
        self.__player2Won = 0

    def player1Won(self):
        self.__player1Won += 1

    def player2Won(self):
        self.__player2Won += 1

    def tied(self):
        self.__tied += 1

    def __str__(self):
        output = ("Tied: {}\n".format(self.__tied)
                  + "Player 1 won: {}\n".format(self.__player1Won)
                  + "Player 2 won: {}".format(self.__player2Won))
        return output



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
            game = play.playGame(random.choice([1, 2]))
            gameState = game.getGameState()

            if gameState.player1Won():
                statistics.player1Won()
            elif gameState.player2Won():
                statistics.player2Won()
            else:
                statistics.tied()

        return statistics

if __name__ == "__main__":
    player1 = Agent.HumanAgent(1)
    player2 = Agent.DecisionTreeAgent(2)

    simulation = Simulation(player1, player2)

    print(simulation.simulate(10000))
