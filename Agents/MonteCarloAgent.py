from Agents.Agent import Agent
import random
from Statistics import Statistics

class MonteCarloAgent(Agent):
    def __init__(self, numberOfGames):
        super().__init__()
        self.numberOfGames = numberOfGames
        self.cache = {}

    def playRandomGame(self, game):
        while game.getGameState().isOngoing():
            randomMove = random.choice(game.getValidMoves())
            game.makeTurn(randomMove)

        return game

    def makeTurn(self, game):
        super().makeTurn(game)

        cacheKey = (game.getState(), self.playerNumber)
        if cacheKey in self.cache:
            return self.cache[cacheKey]

        validMoves = game.getValidMoves()
        statistics = [Statistics() for i in range(len(validMoves))]

        for i, move in enumerate(validMoves):
            gameAfterMove = game.copy()
            gameAfterMove.makeTurn(move)

            for j in range(self.numberOfGames):
                finishedGame = self.playRandomGame(gameAfterMove.copy())
                statistics[i].countGameState(finishedGame.getGameState(), self.playerNumber)

        bestStatistic = 0

        for i, statistic in enumerate(statistics[1:]):
            if statistic.getLosses() < statistics[bestStatistic].getLosses():
                if statistic.getWins() > statistics[bestStatistic].getWins():
                    bestStatistic = i + 1

        self.cache.update({cacheKey: validMoves[bestStatistic]})

        return validMoves[bestStatistic]
