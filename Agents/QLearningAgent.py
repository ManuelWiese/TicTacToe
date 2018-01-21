from Agents.Agent import Agent
import random
import sys


class QFunction:
    def __init__(self):
        self.Q = {}

    def getActionToReward(self, game):
        state = game.getState()

        if state in self.Q:
            return self.Q[state]

        tmpDir = {}
        for move in game.getValidActions():
            tmpDir.update({move: 0})
        self.Q.update({state: tmpDir})

        return self.Q[state]

    def update(self, state, action, target, learningRate):
        self.Q[state][action] += learningRate * (target - self.Q[state][action])


class QLearningAgent(Agent):
    def __init__(self, learningRate, discountFactor, epsilon, collectStatistics=True, qfunction=None):
        super().__init__(collectStatistics)
        self.learningRate = learningRate
        self.discountFactor = discountFactor
        self.epsilon = epsilon

        if qfunction is None:
            self.Q = QFunction()
        else:
            self.Q = qfunction

        self.lastAction = None
        self.lastState = None
        self.training = True

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setTraining(self, training):
        self.training = training

    @staticmethod
    def getBestActions(Qstate):
        bestReward = -sys.maxsize
        bestActions = []

        for action, reward in Qstate.items():
            if reward > bestReward:
                bestReward = reward
                bestActions = [action]
            elif reward == bestReward:
                bestActions.append(action)

        return bestActions

    def getAction(self, game):
        super().getAction(game)

        state = game.getState()
        Qstate = self.Q.getActionToReward(game)

        if random.random() < self.epsilon:
            action = random.choice(list(Qstate))
        else:
            bestActions = self.getBestActions(Qstate)
            action = random.choice(bestActions)

        self.lastAction = action
        self.lastState = state

        assert action in game.getValidActions()

        return action

    def feedbackBeforeTurn(self, game):
        self.updateQ(game)

    def updateQ(self, game):
        if not self.training:
            return

        if self.lastAction is None:
            return

        reward = game.getScore(self.playerNumber)

        if len(game.getValidActions()) > 0:
            Qstate = self.Q.getActionToReward(game)
            optimalFutureReward = max(Qstate.values())
        else:
            optimalFutureReward = 0

        target = (reward + self.discountFactor * optimalFutureReward)

        self.Q.update(self.lastState, self.lastAction, target, self.learningRate)

    def endOfGame(self, game):
        super().endOfGame(game)

        self.updateQ(game)

        self.lastAction = None
        self.lastState = None
