from InvalidMoveError import InvalidMoveError
from CheckArgs import checkIntBetween
from CheckArgs import checkTuple
import copy


class GameState:
    ONGOING, PLAYER1_WON, PLAYER2_WON, TIED = range(4)

    @staticmethod
    def createOngoing():
        return GameState(GameState.ONGOING)

    @staticmethod
    def createPlayer1Won():
        return GameState(GameState.PLAYER1_WON)

    @staticmethod
    def createPlayer2Won():
        return GameState(GameState.PLAYER2_WON)

    @staticmethod
    def createTied():
        return GameState(GameState.TIED)

    def __init__(self, gameState):
        self.gameState = gameState

    def isOngoing(self):
        return self.gameState == GameState.ONGOING

    def isTied(self):
        return self.gameState == GameState.TIED

    def player1Won(self):
        return self.gameState == GameState.PLAYER1_WON

    def player2Won(self):
        return self.gameState == GameState.PLAYER2_WON


class Game:

    def __init__(self, gameLogic, firstTurn=1):
        assert isinstance(gameLogic, GameLogic)
        self.gameLogic = gameLogic
        self.firstTurn = firstTurn
        self.turn = self.firstTurn

    def copy(self):
        newGame = Game(copy.deepcopy(self.gameLogic), self.firstTurn)
        newGame.turn = self.turn

        return newGame

    def makeTurn(self, move):
        if not move in self.gameLogic.getValidMoves():
            raise InvalidMoveError()

        self.gameLogic.makeTurn(move, self.turn)

        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

    def getTurn(self):
        return self.turn

    def getFirstTurn(self):
        return self.firstTurn

    def getGameState(self):
        return self.gameLogic.getGameState()

    def getValidMoves(self):
        return self.gameLogic.getValidMoves()

    def getState(self):
        return hash(self.gameLogic)

    def display(self):
        self.gameLogic.display()

    def getHeuristics(self, playerNumber):
        assert playerNumber == 1 or playerNumber == 2
        return self.gameLogic.getHeuristics(playerNumber)


class GameLogic:

    def __init__(self):
        raise NotImplementedError

    def makeTurn(self, move):
        raise NotImplementedError

    def getGameState(self):
        raise NotImplementedError

    def getValidMoves(self):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError

    def display(self):
        raise NotImplementedError

    def getHeuristics(self, playerNumber):
        raise NotImplementedError


class TicTacToe(GameLogic):

    size = (3, 3)
    winSize = 3

    markers = [' ', 'x', 'o']
    boards = []
    gameStates = []
    validMoves = []

    numberOfStates = len(markers)**(size[0] * size[1])

    def __init__(self):
        if len(TicTacToe.boards) == 0:
            TicTacToe.initStaticLists()

        self.state = 0

    def makeTurn(self, cell, turn):
        assert checkTuple(cell, int, 2)
        assert checkIntBetween(cell[0], 0, TicTacToe.size[0])
        assert checkIntBetween(cell[1], 0, TicTacToe.size[1])

        self.state = TicTacToe.setCell(self.state, cell, turn)


    def getGameState(self):
        return TicTacToe.gameStates[self.state]

    def getValidMoves(self):
        return TicTacToe.validMoves[self.state]

    def __hash__(self):
        return self.state

    def display(self):
        board = TicTacToe.stateToBoard(self.state)
        for row in board:
            print("|", end='')
            for cell in row:
                print("{}|".format(TicTacToe.markers[cell]), end='')
            print("")

    def getHeuristics(self, playerNumber):

        gameState = self.getGameState()

        if playerNumber == 1:
            if gameState.player1Won():
                return 1
            if gameState.player2Won():
                return -1

        if playerNumber == 2:
            if gameState.player1Won():
                return -1
            if gameState.player2Won():
                return 1

        return 0


    @staticmethod
    def calculateBoardFromState(state):
        assert checkIntBetween(state, 0, TicTacToe.numberOfStates)

        board = [[0 for i in range(TicTacToe.size[0])] for j in range(TicTacToe.size[1])]

        for j in range(TicTacToe.size[1]):
            for i in range(TicTacToe.size[0]):
                board[i][j] = state % len(TicTacToe.markers)
                state = (state - board[i][j]) // len(TicTacToe.markers)

        return board

    @staticmethod
    def stateToBoard(state):
        assert checkIntBetween(state, 0, TicTacToe.numberOfStates)
        return TicTacToe.boards[state]

    @staticmethod
    def getCell(state, cell):
        board = TicTacToe.stateToBoard(state)

        assert checkTuple(cell, int, 2)
        assert checkIntBetween(cell[0], 0, TicTacToe.size[0])
        assert checkIntBetween(cell[1], 0, TicTacToe.size[1])

        return board[cell[0]][cell[1]]

    @staticmethod
    def isEmptyCell(state, cell):
        return TicTacToe.getCell(state, cell) == 0

    @staticmethod
    def setCell(state, cell, marker):
        assert checkIntBetween(state, 0, TicTacToe.numberOfStates)

        assert checkTuple(cell, int, 2)
        assert checkIntBetween(cell[0], 0, TicTacToe.size[0])
        assert checkIntBetween(cell[1], 0, TicTacToe.size[1])

        assert checkIntBetween(marker, 0, 3)

        currentValue = TicTacToe.getCell(state, cell)

        base = len(TicTacToe.markers) ** (cell[1] * TicTacToe.size[0] + cell[0])

        state -= base * currentValue
        state += base * marker

        return state

    @staticmethod
    def checkCellDirection(state, cell, direction):

        assert checkTuple(direction, int, 2)

        board = TicTacToe.stateToBoard(state)
        cellValue = TicTacToe.getCell(state, cell)
        counter = 0

        if cellValue == 0:
            return 0

        position = list(cell)
        while True:
            position[0] += direction[0]
            position[1] += direction[1]

            if position[0] >= TicTacToe.size[0] or position[0] < 0:
                return counter
            if position[1] >= TicTacToe.size[1] or position[1] < 0:
                return counter

            if cellValue != board[position[0]][position[1]]:
                return counter

            counter += 1

    @staticmethod
    def checkCell(state, cell):

        assert checkTuple(cell, int, 2)
        assert checkIntBetween(cell[0], 0, TicTacToe.size[0])
        assert checkIntBetween(cell[1], 0, TicTacToe.size[1])

        assert checkIntBetween(state, 0, TicTacToe.numberOfStates)

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        consecutive = 0

        for direction in directions:
            consecutive = max(TicTacToe.checkCellDirection(state, cell, direction)
                              + TicTacToe.checkCellDirection(state, cell,
                                                        (-1 * direction[0],
                                                         -1 * direction[1]))
                              + 1, consecutive)

        return consecutive

    @staticmethod
    def stateToGameState(state):
        assert checkIntBetween(state, 0, TicTacToe.numberOfStates)

        hasFreeCell = False

        for i in range(TicTacToe.size[0]):
            for j in range(TicTacToe.size[1]):
                marker = TicTacToe.getCell(state, (i,j))

                if marker == 0:
                    hasFreeCell = True
                    continue

                consecutive = TicTacToe.checkCell(state, (i,j))

                if consecutive >= TicTacToe.winSize:
                    if marker == 1:
                        return GameState.createPlayer1Won()
                    return GameState.createPlayer2Won()

        if hasFreeCell:
            return GameState.createOngoing()
        return GameState.createTied()


    @staticmethod
    def initStaticLists():
        states = [i for i in range(TicTacToe.numberOfStates)]
        for state in states:
            board = TicTacToe.calculateBoardFromState(state)
            TicTacToe.boards.append(board)
            TicTacToe.gameStates.append(TicTacToe.stateToGameState(state))
            TicTacToe.validMoves.append(TicTacToe.boardToValidMoves(board))


    @staticmethod
    def boardToValidMoves(board):
        validMoves = []
        for row in range(len(board)):
            for column in range(len(board[row])):
                if board[row][column] == 0:
                    validMoves.append((row, column))
        return validMoves
