from Agent import Agent
import random

class RandomAgent(Agent):

    def makeTurn(self, game):
        choices = game.getValidMoves()
        return random.choice(choices)
