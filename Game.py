from InvalidMoveError import InvalidMoveError
from CheckArgs import checkIntBetween
from CheckArgs import checkTuple


class Game:

    size = (3, 3)
    winSize = 3

    ONGOING, WIN1, WIN2, TIE, INVALID = range(5)

    markers = [' ', 'x', 'o']
    boards = []
    gameStates = []

    numberOfStates = len(markers)**(size[0] * size[1])

    @staticmethod
    def calculateBoardFromState(state):
        assert checkIntBetween(state, 0, Game.numberOfStates)

        board = [[0 for i in range(Game.size[0])] for j in range(Game.size[1])]

        for j in range(Game.size[1]):
            for i in range(Game.size[0]):
                board[i][j] = state % len(Game.markers)
                state = (state - board[i][j]) // len(Game.markers)

        return board

    @staticmethod
    def stateToBoard(state):
        assert checkIntBetween(state, 0, Game.numberOfStates)
        return Game.boards[state]

    @staticmethod
    def getCell(state, cell):
        board = Game.stateToBoard(state)

        assert checkTuple(cell, int, 2)
        assert checkIntBetween(cell[0], 0, Game.size[0])
        assert checkIntBetween(cell[1], 0, Game.size[1])

        return board[cell[0]][cell[1]]

    @staticmethod
    def isEmptyCell(state, cell):
        return Game.getCell(state, cell) == 0

    @staticmethod
    def setCell(state, cell, marker):
        assert checkIntBetween(state, 0, Game.numberOfStates)

        assert checkTuple(cell, int, 2)
        assert checkIntBetween(cell[0], 0, Game.size[0])
        assert checkIntBetween(cell[1], 0, Game.size[1])

        assert checkIntBetween(marker, 0, 3)

        currentValue = Game.getCell(state, cell)

        base = len(Game.markers) ** (cell[1] * Game.size[0] + cell[0])

        state -= base * currentValue
        state += base * marker

        return state

    @staticmethod
    def checkCellDirection(state, cell, direction):

        assert checkTuple(direction, int, 2)

        board = Game.stateToBoard(state)
        cellValue = Game.getCell(state, cell)
        counter = 0

        if cellValue == 0:
            return 0

        position = list(cell)
        while True:
            position[0] += direction[0]
            position[1] += direction[1]

            if position[0] >= Game.size[0] or position[0] < 0:
                return counter
            if position[1] >= Game.size[1] or position[1] < 0:
                return counter

            if cellValue != board[position[0]][position[1]]:
                return counter

            counter += 1

    @staticmethod
    def checkCell(state, cell):

        assert checkTuple(cell, int, 2)
        assert checkIntBetween(cell[0], 0, Game.size[0])
        assert checkIntBetween(cell[1], 0, Game.size[1])

        assert checkIntBetween(state, 0, Game.numberOfStates)

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        consecutive = 0

        for direction in directions:
            consecutive = max(Game.checkCellDirection(state, cell, direction)
                              + Game.checkCellDirection(state, cell,
                                                        (-1 * direction[0],
                                                         -1 * direction[1]))
                              + 1, consecutive)

        return consecutive

    @staticmethod
    def stateToGameState(state):
        assert checkIntBetween(state, 0, Game.numberOfStates)

        hasFreeCell = False

        for i in range(Game.size[0]):
            for j in range(Game.size[1]):
                marker = Game.getCell(state, (i,j))

                if marker == 0:
                    hasFreeCell = True
                    continue

                consecutive = Game.checkCell(state, (i,j))

                if consecutive >= Game.winSize:
                    if marker == 1:
                        return Game.WIN1
                    return Game.WIN2

        if hasFreeCell:
            return Game.ONGOING
        return Game.TIE

    @staticmethod
    def loadGamestates():
        states = [i for i in range(Game.numberOfStates)]
        for state in states:
            Game.boards.append(Game.calculateBoardFromState(state))
            Game.gameStates.append(Game.stateToGameState(state))

    def __init__(self, firstTurn=1):
        if len(Game.boards) == 0:
            Game.loadGamestates()

        self.state = 0
        self.firstTurn = firstTurn
        self.turn = self.firstTurn

    def copy(self):
        newGame = Game()

        newGame.state = self.state
        newGame.firstTurn = self.firstTurn
        newGame.turn = self.turn

        return newGame

    def getState(self):
        return self.state

    def getTurn(self):
        return self.turn

    def getBoard(self):
        return Game.stateToBoard(self.state)

    def getGameState(self):
        return Game.gameStates[self.state]

    def getValidMoves(self):
        board = self.getBoard()
        validMoves = []
        for row in range(len(board)):
            for column in range(len(board[row])):
                if board[row][column] == 0:
                    validMoves.append((row, column))

        return validMoves

    def makeTurn(self, cell):
        assert checkTuple(cell, int, 2)
        assert checkIntBetween(cell[0], 0, Game.size[0])
        assert checkIntBetween(cell[1], 0, Game.size[1])

        if not Game.isEmptyCell(self.state, cell):
            raise InvalidMoveError()

        self.state = Game.setCell(self.state, cell, self.turn)

        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

    def displayBoard(self):
        board = Game.stateToBoard(self.state)
        print("Playerturn: {}".format(self.turn))
        for row in board:
            print("|", end='')
            for cell in row:
                print("{}|".format(Game.markers[cell]), end='')
            print("")
