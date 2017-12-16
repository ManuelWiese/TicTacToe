from Agents.Agent import Agent
import random

class QLearningAgent(Agent):
    def __init__(self, learningRate, discountFactor, epsilon):
        super().__init__()
        self.learningRate = learningRate
        self.discountFactor = discountFactor
        self.epsilon = epsilon
        self.Q = {}
        self.lastMove = None
        self.lastState = None

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def makeTurn(self, game):
        super().makeTurn(game)

        state = game.getState()
        Qstate = self.getQ(game)

        if random.random() < self.epsilon:
            move = random.choice(list(Qstate))
        else:
            maxKeyValuePair = max(Qstate.items(), key = lambda x: x[1])
            move = maxKeyValuePair[0]

        self.lastMove = move
        self.lastState = state

        assert move in game.getValidMoves()

        return move

    def getQ(self, game):
        state = game.getState()

        if state in self.Q:
            return self.Q[state]

        tmpDir = {}
        for move in game.getValidMoves():
            tmpDir.update({move : 0})
        self.Q.update({state : tmpDir})
        return self.Q[state]


    def feedbackAfterOpponentsTurn(self, game):
        self.updateQ(game)


    def updateQ(self, game):
        if self.lastMove is None:
            return

        reward = game.getHeuristics(self.playerNumber)

        if game.getState() in self.Q:
            Qstate = self.Q[game.getState()]
            optimalFutureValue = max(Qstate.values())
        else:
            optimalFutureValue = 0

        self.Q[self.lastState][self.lastMove] = ((1 - self.learningRate) * self.Q[self.lastState][self.lastMove]
                                                 + self.learningRate * (reward + self.discountFactor * optimalFutureValue))

    def endOfGame(self, game):
        self.updateQ(game)

        self.lastMove = None
        self.lastState = None
