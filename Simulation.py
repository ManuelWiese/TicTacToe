import random

from Agents.NeatAgent import NeatAgent
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

from utils.FloatRange import FloatRange


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
    runsPerGenome = 1000
    players = [NeatAgent(TicTacToe, runsPerGenome), RandomAgent()]

    simulation = Simulation(TicTacToe, players)

    runs = 150 * 200
    for _ in range(runs):

        simulation.simulate(runsPerGenome)
        print(players[0].getStatistics())
        players[0].resetStatistics()

    players[0].setTraining(False)
    simulation = Simulation(TicTacToe, [players[0], RandomAgent()])
    simulation.simulate(runsPerGenome*10)

    print(players[0].getStatistics())

    players[0].pool.plotBestGenomeOfGeneration()

    while True:
        # pass
        players[0].pool.bestGenomeOfGeneration[-1].plotNetwork()