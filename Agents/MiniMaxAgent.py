from Agents.Agent import Agent
import sys

class MiniMaxAgent(Agent):
    def __init__(self, playerNumber, depth):
        super().__init__(playerNumber)
        self.depth = depth
        self.cache = {}

    def minimax(self, game, depth):
        cacheKey = (game.getState(), game.getTurn())
        if cacheKey in self.cache:
            return self.cache[cacheKey]

        if depth == 0 or not game.getGameState().isOngoing():
            return game.getHeuristics(self.playerNumber)

        if game.getTurn() == self.playerNumber:
            bestValue = -sys.maxsize
        else:
            bestValue = sys.maxsize

        validMoves = game.getValidMoves()

        for move in validMoves:
            copiedGame = game.copy()
            copiedGame.makeTurn(move)

            value = self.minimax(copiedGame, depth-1)
            if game.getTurn() == self.playerNumber:
                bestValue = max(value, bestValue)
            else:
                bestValue = min(value, bestValue)

        self.cache.update({cacheKey: bestValue})
        return bestValue


    def makeTurn(self, game):
        validMoves = game.getValidMoves()

        bestMove = validMoves[0]
        bestValue = -sys.maxsize
        for move in validMoves:
            copiedGame = game.copy()
            copiedGame.makeTurn(move)

            value = self.minimax(copiedGame, self.depth)
            if value > bestValue:
                bestMove = move
                bestValue = value

        return bestMove
