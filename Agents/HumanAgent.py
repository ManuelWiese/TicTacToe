from Agents.Agent import Agent
from InvalidMoveError import InvalidMoveError

class HumanAgent(Agent):

    def makeTurn(self, game):
        super().makeTurn(game)

        print("Player {}, it's your turn".format(game.getTurn()))
        game.display()
        turn = input("please enter your move in the format <row> <column>: ").split()
        try:
            turn = [int(x) for x in turn]
            return tuple(turn)
        except:
            print("{} is not a valid input".format(turn))
            return self.makeTurn(game)


    def wasInvalidTurn(self, game, turn):
        print("your input '{}' is invalid".format(turn))
        print("Valid moves: {}".format(game.getValidMoves()))

    def endOfGame(self, game):
        super().endOfGame(game)

        if game.getGameState().isTied():
            print("Game is tied")
        elif game.getGameState().player1Won():
            print("Player 1 wins")
        elif game.getGameState().player2Won():
            print("Player 2 wins")

        game.display()
