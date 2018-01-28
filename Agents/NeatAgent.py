import random
import sys

from Agents import neat
from Agents.Agent import Agent


class NeatAgent(Agent):
    def __init__(self, GameClass, runsPerGenome, collectStatistics=True):
        super().__init__(collectStatistics)

        self.GameClass = GameClass
        self.pool = neat.Pool(inputs=GameClass.getObservationSize(),
                              outputs=GameClass.getActionSpaceSize())
        self.runsPerGenome = runsPerGenome
        self.run = 0
        self.fitness = 0

        self.training = True

    def setTraining(self, training):
        self.training = training

    def getAction(self, game):
        super().getAction(game)

        if self.training:
            genome = self.pool.species[self.pool.currentSpecies].genomes[self.pool.currentGenome]
        else:
            genome = self.pool.bestGenomeOfGeneration[-1]

        output = genome.evaluate(game.getObservation())
        validActions = game.getValidActions()
        actionSpace = game.getActionSpace()

        maxP = -sys.maxsize
        bestActions = []
        for index, p in enumerate(output):
            if actionSpace[index] not in validActions:
                continue

            if p > maxP:
                bestActions = [actionSpace[index]]
                maxP = p

            if p == maxP:
                bestActions.append(actionSpace[index])

        return random.choice(bestActions)

    def endOfGame(self, game):
        super().endOfGame(game)
        self.fitness += game.getScore(self.playerNumber)
        self.run += 1

        if self.run == self.runsPerGenome:
            genome = self.pool.species[self.pool.currentSpecies].genomes[self.pool.currentGenome]

            self.run = 0

            genome.fitness = self.fitness / self.runsPerGenome
            self.fitness = 0

            self.pool.nextGenome()

