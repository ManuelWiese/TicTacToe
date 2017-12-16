from Agents.Agent import Agent
import random

class RandomAgent(Agent):

    def makeTurn(self, game):
        super().makeTurn(game)

        choices = game.getValidMoves()
        return random.choice(choices)
