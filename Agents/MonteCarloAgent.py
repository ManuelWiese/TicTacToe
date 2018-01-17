from Agents.Agent import Agent
import random
from Statistics import Statistics

class MonteCarloAgent(Agent):
    def __init__(self, numberOfGames):
        super().__init__()
        self.numberOfGames = numberOfGames
        self.cache = {}

    def playRandomGame(self, game):
        while game.getGameStatus().isOngoing():
            randomMove = random.choice(game.getValidActions())
            game.makeMove(randomMove)

        return game

    def getAction(self, game):
        super().getAction(game)

        cacheKey = (game.getState(), self.playerNumber)
        if cacheKey in self.cache:
            return self.cache[cacheKey]

        validMoves = game.getValidActions()
        statistics = [Statistics() for i in range(len(validMoves))]

        for i, move in enumerate(validMoves):
            gameAfterMove = game.copy()
            gameAfterMove.makeMove(move)

            for j in range(self.numberOfGames):
                finishedGame = self.playRandomGame(gameAfterMove.copy())
                statistics[i].countGameState(finishedGame.getGameStatus(), self.playerNumber)

        bestStatistic = 0

        for i, statistic in enumerate(statistics[1:]):
            if statistic.getLosses() < statistics[bestStatistic].getLosses():
                if statistic.getWins() > statistics[bestStatistic].getWins():
                    bestStatistic = i + 1

        self.cache.update({cacheKey: validMoves[bestStatistic]})

        return validMoves[bestStatistic]
