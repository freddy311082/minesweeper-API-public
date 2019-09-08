from django.test import TestCase

from minesweeper.core.board import GameBoard
from minesweeper.core.cell import CellObjectFactory, CellObjectType, CellState, RevealCellResult
from minesweeper.core.game import MinesweeperGame, GameState

TOTAL_ROWS = 50
TOTAL_COLS = 50
TOTAL_MINES = 15

class CellTests(TestCase):

    def test_EmptyCell_CanBeRevealed_RevealedCellsCannotBeRevealed(self):
        empty_cell = CellObjectFactory.instance(CellObjectType.EMPTY, row=0, col=0, state=CellState.REVEALED)
        self.assertFalse(empty_cell.can_be_revealed())

        mine_cell = CellObjectFactory.instance(CellObjectType.MINE, row=0, col=0, state=CellState.REVEALED)
        self.assertFalse(mine_cell.can_be_revealed())

    def test_EmptyCell_NonRevealedCellsCanBeRevealed(self):
        empty_cell = CellObjectFactory.instance(CellObjectType.EMPTY, row=0, col=0, state=CellState.HIDED)
        self.assertTrue(empty_cell.can_be_revealed())

        mine_cell = CellObjectFactory.instance(CellObjectType.MINE, row=0, col=0, state=CellState.HIDED)
        self.assertTrue(mine_cell.can_be_revealed())

    def test_EmptyCell_IsEligibleToRevealBorder_FalseIfExistsAtLeastOneMineInTheBorder(self):
        empty_cell = CellObjectFactory.instance(CellObjectType.EMPTY, row=0, col=0, state=CellState.HIDED,
                                                total_mines_in_border=1)
        self.assertFalse(empty_cell.is_eligible_to_reveal_border())

    def test_EmptyCell_IsEligibleToRevealBorder_TrueIfDoesntHaveAtLeastOneMineInTheBorder(self):
        empty_cell = CellObjectFactory.instance(CellObjectType.EMPTY, row=0, col=0, state=CellState.HIDED)
        self.assertTrue(empty_cell.is_eligible_to_reveal_border())

    def test_MineCell_WillNeverBeEligibleToRevealBorder(self):
        mine_cell = CellObjectFactory.instance(CellObjectType.MINE, row=0, col=0, state=CellState.HIDED)
        self.assertFalse(mine_cell.is_eligible_to_reveal_border())

    def test_RevealCellResult(self):
        empty_cell = CellObjectFactory.instance(CellObjectType.EMPTY, row=0, col=0, state=CellState.HIDED)
        self.assertEqual(empty_cell.reveal(), RevealCellResult.ALIVE)

        mine_cell = CellObjectFactory.instance(CellObjectType.MINE, row=0, col=0, state=CellState.HIDED)
        self.assertEqual(mine_cell.reveal(), RevealCellResult.LOST)


class GameBoardTest(TestCase):

    def test_removeAllMines(self):
        board = GameBoard(TOTAL_ROWS, TOTAL_COLS)
        board.add_mine(0, 0)
        board.add_mine(5, 5)
        board.remove_mines()

        self.assertEqual(board.mines_number, 0)
        for i in range(board.rows):
            for j in range(board.cols):
                self.assertFalse(board.cell(i, j).is_a_mine())

    def test_reveal_all(self):
        board = GameBoard(TOTAL_ROWS, TOTAL_COLS)
        board.add_mine(0, 0)
        board.add_mine(5, 5)
        board.reveal_all()

        for i in range(TOTAL_ROWS):
            for j in range(TOTAL_COLS):
                self.assertEqual(board.cell(i, j).state, CellState.REVEALED)


class GameTest(TestCase):

    def test_CreateGame_RaiseExceptionIfAtLeastOneParamIsNotValid(self):
        # invalid rows number
        with self.assertRaises(ValueError):
            game = MinesweeperGame(-3, 50, 10, state=GameState.NEW)

        # invalid cols number
        with self.assertRaises(ValueError):
            game = MinesweeperGame(50, -3, 10, state=GameState.NEW)

        # invalid mines number
        with self.assertRaises(ValueError):
            game = MinesweeperGame(50, 50, -8, state=GameState.NEW)

    def test_CreateGame_ValidIfAllEmptyCellsAndMinesWereCreated(self):
        game = MinesweeperGame(TOTAL_ROWS, TOTAL_COLS, TOTAL_MINES, state=GameState.NEW)

        total_mines = 0
        for i in range(game.board.rows):
            for j in range(game.board.cols):
                cell = game.cell(i, j)
                self.assertEqual(cell.state, CellState.HIDED)

                if cell.is_a_mine():
                    total_mines += 1

        self.assertEqual(total_mines, TOTAL_MINES)

    def test_RevealCell_FailIfCellPositionIsNotValid(self):
        game = MinesweeperGame(TOTAL_ROWS, TOTAL_COLS, 1, state=GameState.NEW)
        game.reveal(-1, 4)
