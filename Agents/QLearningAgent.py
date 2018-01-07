from Agents.Agent import Agent
import random
import sys


class QLearningAgent(Agent):
    def __init__(self, learningRate, discountFactor, epsilon):
        super().__init__()
        self.learningRate = learningRate
        self.discountFactor = discountFactor
        self.epsilon = epsilon
        self.Q = {}
        self.lastMove = None
        self.lastState = None
        self.training = True

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setTraining(self, training):
        self.training = training

    @staticmethod
    def getBestMoves(Qstate):
        bestReward = -sys.maxsize
        bestMoves = []

        for move, reward in Qstate.items():
            if reward > bestReward:
                bestReward = reward
                bestMoves = [move]
            elif reward == bestReward:
                bestMoves.append(move)

        return bestMoves

    def makeTurn(self, game):
        super().makeTurn(game)

        state = game.getState()
        Qstate = self.getQ(game)

        if random.random() < self.epsilon:
            move = random.choice(list(Qstate))
        else:
            bestMoves = self.getBestMoves(Qstate)
            move = random.choice(bestMoves)

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
            tmpDir.update({move: 0})
        self.Q.update({state: tmpDir})
        return self.Q[state]

    def feedbackAfterOpponentsTurn(self, game):
        self.updateQ(game)

    def updateQ(self, game):
        if not self.training:
            return

        if self.lastMove is None:
            return

        reward = game.getHeuristics(self.playerNumber)

        if game.getState() in self.Q:
            Qstate = self.Q[game.getState()]
            optimalFutureValue = max(Qstate.values())
        else:
            optimalFutureValue = 0

        self.Q[self.lastState][self.lastMove] = ((1 - self.learningRate)
                                                 * self.Q[self.lastState][self.lastMove]
                                                 + self.learningRate
                                                 * (reward + self.discountFactor * optimalFutureValue))

    def endOfGame(self, game):
        super().endOfGame(game)

        self.updateQ(game)

        self.lastMove = None
        self.lastState = None
