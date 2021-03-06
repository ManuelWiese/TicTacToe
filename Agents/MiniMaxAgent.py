from Agents.Agent import Agent
import sys

class MiniMaxAgent(Agent):
    def __init__(self, depth, collectStatistics=True):
        super().__init__(collectStatistics)
        self.depth = depth
        self.cache = {}

    def minimax(self, game, depth):
        cacheKey = (game.getState(), self.playerNumber)
        if cacheKey in self.cache:
            return self.cache[cacheKey]

        if depth == 0 or not game.getGameStatus().isOngoing():
            return game.getScore(self.playerNumber)

        if game.getTurn() == self.playerNumber:
            bestValue = -sys.maxsize
        else:
            bestValue = sys.maxsize

        validMoves = game.getValidActions()

        for move in validMoves:
            copiedGame = game.copy()
            copiedGame.makeMove(move)

            value = self.minimax(copiedGame, depth-1)
            if game.getTurn() == self.playerNumber:
                bestValue = max(value, bestValue)
            else:
                bestValue = min(value, bestValue)

        self.cache.update({cacheKey: bestValue})
        return bestValue


    def getAction(self, game):
        super().getAction(game)

        validMoves = game.getValidActions()

        bestMove = validMoves[0]
        bestValue = -sys.maxsize
        for move in validMoves:
            copiedGame = game.copy()
            copiedGame.makeMove(move)

            value = self.minimax(copiedGame, self.depth)
            if value > bestValue:
                bestMove = move
                bestValue = value

        return bestMove
