from Agents.Agent import Agent

class DecisionTreeAgent(Agent):

    TIE, PLAYER_1_WINS, PLAYER_2_WINS = range(3)

    @staticmethod
    def allElementsEqual(someList):
        return len(set(someList)) <= 1

    def __init__(self):
        super().__init__()
        self.gameConfigurationToWinPrediction = {}

    def winPrediction(self, game):
        gameConfiguration = (game.getState(), game.getTurn())
        if gameConfiguration in self.gameConfigurationToWinPrediction:
            return self.gameConfigurationToWinPrediction[gameConfiguration]

        gameState = game.getGameState()
        if not gameState.isOngoing():
            if gameState.isTied():
                return DecisionTreeAgent.TIE
            return gameState.getWinner()

        choices = game.getValidMoves()
        predictions = []

        for choice in choices:
            newGame = game.copy()
            newGame.makeTurn(choice)

            predictions.append(self.winPrediction(newGame))

        if game.getTurn() in predictions:
            prediction = game.getTurn()
        elif DecisionTreeAgent.allElementsEqual(predictions) and predictions[0] != DecisionTreeAgent.TIE:
            prediction = predictions[0]
        else:
            prediction = DecisionTreeAgent.TIE

        self.gameConfigurationToWinPrediction.update({gameConfiguration: prediction})

        return prediction

    def makeTurn(self, game):
        super().makeTurn(game)

        prediction = self.winPrediction(game)
        choices = game.getValidMoves()

        for choice in choices:
            newGame = game.copy()
            newGame.makeTurn(choice)
            if self.winPrediction(newGame) == prediction:
                return choice
