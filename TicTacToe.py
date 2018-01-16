from InvalidMoveError import InvalidMoveError

from GameState import GameState

from CheckArgs import checkIntBetween
from CheckArgs import checkTuple

from Game import Game


class TicTacToe(Game):
    PLAYERCOUNT = 2

    PLAYER1 = 0
    PLAYER2 = 1

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

        self.turn = TicTacToe.PLAYER1

        self.state = 0

    def copy(self):
        copied = TicTacToe()
        copied.state = self.state
        copied.turn = self.turn

        return copied

    @staticmethod
    def getPlayerCount():
        return TicTacToe.PLAYERCOUNT

    def makeTurn(self, cell):
        assert checkTuple(cell, int, 2)
        assert checkIntBetween(cell[0], 0, TicTacToe.size[0])
        assert checkIntBetween(cell[1], 0, TicTacToe.size[1])
        if cell not in self.getValidMoves():
            raise InvalidMoveError()

        marker = self.turn + 1
        self.state = TicTacToe.setCell(self.state, cell, marker)

        if self.turn == TicTacToe.PLAYER1:
            self.turn = TicTacToe.PLAYER2
        else:
            self.turn = TicTacToe.PLAYER1

    def getTurn(self):
        return self.turn

    def getGameState(self):
        return TicTacToe.gameStates[self.state]

    def getValidMoves(self):
        return TicTacToe.validMoves[self.state]

    def getState(self):
        return self.state

    def display(self):
        board = TicTacToe.stateToBoard(self.state)
        for row in board:
            print("|", end='')
            for cell in row:
                print("{}|".format(TicTacToe.markers[cell]), end='')
            print("")

    def getHeuristics(self, playerNumber):
        assert playerNumber == TicTacToe.PLAYER1 or playerNumber == TicTacToe.PLAYER2

        gameState = self.getGameState()

        if gameState.isOngoing() or gameState.isTied():
            return 0

        if gameState.didPlayerWin(playerNumber):
            return 1
        else:
            return -1

    @staticmethod
    def calculateBoardFromState(state):
        assert checkIntBetween(state, 0, TicTacToe.numberOfStates)

        board = [[0 for i in range(TicTacToe.size[0])]
                 for j in range(TicTacToe.size[1])]

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
        assert checkIntBetween(state, 0, TicTacToe.numberOfStates)

        assert checkTuple(cell, int, 2)
        assert checkIntBetween(cell[0], 0, TicTacToe.size[0])
        assert checkIntBetween(cell[1], 0, TicTacToe.size[1])

        board = TicTacToe.stateToBoard(state)

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
    def consecutiveInDirection(state, cell, direction):
        assert checkIntBetween(state, 0, TicTacToe.numberOfStates)

        assert checkTuple(cell, int, 2)
        assert checkIntBetween(cell[0], 0, TicTacToe.size[0])
        assert checkIntBetween(cell[1], 0, TicTacToe.size[1])

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
    def maxConsecutive(state, cell):
        assert checkIntBetween(state, 0, TicTacToe.numberOfStates)

        assert checkTuple(cell, int, 2)
        assert checkIntBetween(cell[0], 0, TicTacToe.size[0])
        assert checkIntBetween(cell[1], 0, TicTacToe.size[1])

        assert checkIntBetween(state, 0, TicTacToe.numberOfStates)

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        maxConsecutive = 0

        for direction in directions:
            consecutiveInDirection = TicTacToe.consecutiveInDirection(
                state,
                cell,
                direction)

            consecutiveInOppositeDirection = TicTacToe.consecutiveInDirection(
                state,
                cell,
                (-1 * direction[0], -1 * direction[1]))

            maxConsecutive = max(consecutiveInDirection
                                 + consecutiveInOppositeDirection
                                 + 1
                                 , maxConsecutive)

        return maxConsecutive

    @staticmethod
    def stateToGameState(state):
        assert checkIntBetween(state, 0, TicTacToe.numberOfStates)

        hasFreeCell = False

        for i in range(TicTacToe.size[0]):
            for j in range(TicTacToe.size[1]):
                marker = TicTacToe.getCell(state, (i, j))

                if marker == 0:
                    hasFreeCell = True
                    continue

                maxConsecutive = TicTacToe.maxConsecutive(state, (i, j))

                if maxConsecutive >= TicTacToe.winSize:
                    if marker == 1:
                        return GameState.createPlayerWon(TicTacToe.PLAYER1)
                    return GameState.createPlayerWon(TicTacToe.PLAYER2)

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
        assert isinstance(board, list)

        validMoves = []
        for row in range(len(board)):
            for column in range(len(board[row])):
                if board[row][column] == 0:
                    validMoves.append((row, column))
        return validMoves
