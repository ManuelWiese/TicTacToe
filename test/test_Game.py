from Game import Game
import unittest
from InvalidMoveError import InvalidMoveError

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_calculateBoardFromStateTypeError(self):
        self.assertRaises(AssertionError, Game.calculateBoardFromState, 1.4)

    def test_calculateBoardFromStateValueError(self):
        self.assertRaises(AssertionError, Game.calculateBoardFromState, -1)

    def test_calculateBoardFromState(self):
        result = Game.calculateBoardFromState(13)
        self.assertEqual([[1, 0, 0], [1, 0, 0], [1, 0, 0]], result)

    def test_checkCellDirectionTypeError(self):
        self.assertRaises(AssertionError, Game.checkCellDirection, "1", (1, 1), (0, 1))
        self.assertRaises(AssertionError, Game.checkCellDirection,  1, 1, (0, 1))
        self.assertRaises(AssertionError, Game.checkCellDirection,  1, (1, 1), 1)

    def test_checkCellDirectionValueError(self):
        self.assertRaises(AssertionError, Game.checkCellDirection, -1, (1, 1), (0, 1))
        self.assertRaises(AssertionError, Game.checkCellDirection, len(Game.markers)**(Game.size[0]*Game.size[1]), (1, 1), (0, 1))
        self.assertRaises(AssertionError, Game.checkCellDirection,  1, (1, 1, 1), (0, 1))
        self.assertRaises(AssertionError, Game.checkCellDirection,  1, (1, Game.size[1]), (0, 1))
        self.assertRaises(AssertionError, Game.checkCellDirection,  1, (1, 1), (1,))

    def test_checkCellTypeError(self):
        self.assertRaises(AssertionError, Game.checkCell, "1", (1, 1))
        self.assertRaises(AssertionError, Game.checkCell, 1, 1)

    def test_checkCellValueError(self):
        self.assertRaises(AssertionError, Game.checkCell, -1, (1, 1))
        self.assertRaises(AssertionError, Game.checkCell, 1, (1, Game.size[1]))

    def test_checkCell(self):
        result = Game.checkCell(122, (0, 1))
        self.assertEqual(2, result)

    def test_stateToGameStateTypeError(self):
        self.assertRaises(AssertionError, Game.stateToGameState, "1")

    def test_stateToGameStateValueError(self):
        self.assertRaises(AssertionError, Game.stateToGameState, -1)

    def test_stateToGameState(self):
        result = Game.stateToGameState(13)
        self.assertEqual(Game.WIN1, result)

        result = Game.stateToGameState(26)
        self.assertEqual(Game.WIN2, result)

        result = Game.stateToGameState(14)
        self.assertEqual(Game.ONGOING, result)

    def test_getCellTypeError(self):
        self.assertRaises(AssertionError, Game.getCell, "0", (1, 1))
        self.assertRaises(AssertionError, Game.getCell, 0, "1")

    def test_getCellValueError(self):
        self.assertRaises(AssertionError, Game.getCell, -1, (1, 1))
        self.assertRaises(AssertionError, Game.getCell, 0, (-1, 1))

    def test_getCell(self):
        result = Game.getCell(13, (0, 0))
        self.assertEqual(1, result)
        result = Game.getCell(13, (1, 1))
        self.assertEqual(0, result)
        result = Game.getCell(14, (0, 0))
        self.assertEqual(2, result)

    def test_makeTurnTypeError(self):
        self.assertRaises(AssertionError, self.game.makeTurn, "0")

    def test_makeTurnValueError(self):
        self.assertRaises(AssertionError, self.game.makeTurn, (-1, -1))

    def test_makeTurnInvalidMoveError(self):
        self.game.state = 1
        self.game.turn = 1
        self.assertRaises(InvalidMoveError, self.game.makeTurn, (0, 0))

    def test_makeTurn(self):
        self.game.state = 0
        self.game.turn = 1
        self.game.makeTurn((0, 0))

        self.assertEqual(1, self.game.state)
        self.assertEqual(2, self.game.turn)

    def test_setCellTypeError(self):
        self.assertRaises(AssertionError, Game.setCell, "1", (1, 1), 1)
        self.assertRaises(AssertionError, Game.setCell, 1, 1, 1)
        self.assertRaises(AssertionError, Game.setCell, 1, (1, 1), "1")

    def test_setCellValueError(self):
        self.assertRaises(AssertionError, Game.setCell, -1, (1, 1), 1)
        self.assertRaises(AssertionError, Game.setCell, 1, (-1,1), 1)
        self.assertRaises(AssertionError, Game.setCell, 1, (1, 1), -1)

    def test_setCell(self):
        result = Game.setCell(0, (0, 0), 1)
        self.assertEqual(1, result)

        result = Game.setCell(0, (0, 0), 2)
        self.assertEqual(2, result)

        result = Game.setCell(0, (2, 0), 1)
        self.assertEqual(9, result)

        result = Game.setCell(0, (2, 0), 2)
        self.assertEqual(18, result)
