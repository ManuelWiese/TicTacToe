from Agents.Agent import Agent
import random

class RandomAgent(Agent):

    def getAction(self, game):
        super().getAction(game)

        choices = game.getValidActions()
        return random.choice(choices)
