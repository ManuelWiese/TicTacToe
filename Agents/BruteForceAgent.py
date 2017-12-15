from Agents.Agent import Agent

class BruteForceAgent(Agent):

    def __init__(self, playerNumber):
        super().__init__(playerNumber)
        self.cache = {}

    def winProbability(self, game):
        cacheKey = (game.getState(), game.getTurn())

        if cacheKey in self.cache:
            return self.cache[cacheKey]

        gameState = game.getGameState()
        if not gameState.isOngoing():
            if gameState.player1Won():
                return [1, 0, 0]
            if gameState.player2Won():
                return [0, 1, 0]
            return [0, 0, 1]

        choices = game.getValidMoves()
        rates = [0, 0, 0]

        for choice in choices:
            newGame = game.copy()
            newGame.makeTurn(choice)

            probability = self.winProbability(newGame)
            rates[0] += probability[0] / len(choices)
            rates[1] += probability[1] / len(choices)
            rates[2] += probability[2] / len(choices)

        assert abs(sum(rates) - 1) < 0.001, "probabilities are not normalized, instead {}".format(sum(rates))

        self.cache.update({cacheKey: rates})

        return rates

    def makeTurn(self, game):
        choices = game.getValidMoves()

        rates = []
        for choice in choices:
            newGame = game.copy()
            newGame.makeTurn(choice)
            rates.append(self.winProbability(newGame))

        bestChoiceIndex = self.getBestCoiceIndex(rates)

        return choices[bestChoiceIndex]

    def getBestCoiceIndex(self, rates):
        pass


class BruteForceAgentMaximizeWins(BruteForceAgent):
    def getBestCoiceIndex(self, rates):
        winRates = [x[self.playerNumber - 1] for x in rates]
        bestChoiceIndex, _ = max(enumerate(winRates), key = lambda x: x[1])

        return bestChoiceIndex


class BruteForceAgentMinimizeLosses(BruteForceAgent):
    def getBestCoiceIndex(self, rates):
        winRates = [x[self.playerNumber % 2] for x in rates]
        bestChoiceIndex, _ = min(enumerate(winRates), key = lambda x: x[1])

        return bestChoiceIndex


class BruteForceAgentBalanced(BruteForceAgent):
    def __init__(self, playerNumber, win, loss, tie):
        super().__init__(playerNumber)
        self.win = win
        self.loss = loss
        self.tie = tie

    def getBestCoiceIndex(self, rates):
        quantifier = []
        for rate in rates:
            quantifier.append(self.win * rate[self.playerNumber-1] +
                              self.loss * rate[self.playerNumber%2] +
                              self.tie * rate[2])

        bestChoiceIndex, _ = max(enumerate(quantifier), key = lambda x : x[1])

        return bestChoiceIndex
