from Agent import Agent
import random

class QLearningAgent(Agent):
    def __init__(self, playerNumber, learningRate, discountFactor, epsilon):
        super().__init__(playerNumber)
        self.learningRate = learningRate
        self.discountFactor = discountFactor
        self.epsilon = epsilon
        self.Q = {}
        self.lastMove = None
        self.lastState = None

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def makeTurn(self, game):

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


    def feedback(self, game):
        if self.lastMove is None:
            return

        # AFTER opponents turn or after agents turn when finished
        if game.getTurn() == self.playerNumber or not game.getGameState().isOngoing():
            reward = game.getHeuristics(self.playerNumber)

            if game.getState() in self.Q:
                Qstate = self.Q[game.getState()]
                optimalFutureValue = max(Qstate.values())
            else:
                optimalFutureValue = 0

            self.Q[self.lastState][self.lastMove] = ((1 - self.learningRate) * self.Q[self.lastState][self.lastMove]
                                                     + self.learningRate * (reward + self.discountFactor * optimalFutureValue))

    def getQ(self, game):
        state = game.getState()

        if state in self.Q:
            return self.Q[state]

        tmpDir = {}
        for move in game.getValidMoves():
            tmpDir.update({move : 0})
        self.Q.update({state : tmpDir})
        return self.Q[state]

    def endOfGame(self, game):
        self.lastMove = None
        self.lastState = None
