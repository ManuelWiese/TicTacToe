from Agents.Agent import Agent
from InvalidMoveError import InvalidMoveError

class HumanAgent(Agent):

    def getAction(self, game):
        super().getAction(game)

        print("Player {}, it's your turn".format(game.getTurn()))
        game.display()
        turn = input("please enter your move in the format <row> <column>: ").split()
        try:
            turn = [int(x) for x in turn]
            return tuple(turn)
        except:
            print("{} is not a valid input".format(turn))
            return self.getAction(game)


    def wasInvalidTurn(self, game, turn):
        print("your input '{}' is invalid".format(turn))
        print("Valid moves: {}".format(game.getValidActions()))

    def endOfGame(self, game):
        super().endOfGame(game)

        gameState = game.getGameState()

        if gameState.isTied():
            print("Game is tied")
        print("Player {} wins".format(gameState.getWinner))

        game.display()
