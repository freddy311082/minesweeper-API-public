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
        self.assertFalse(empty_cell.is_eligible_to_reveal_borders())

    def test_EmptyCell_IsEligibleToRevealBorder_TrueIfDoesntHaveAtLeastOneMineInTheBorder(self):
        empty_cell = CellObjectFactory.instance(CellObjectType.EMPTY, row=0, col=0, state=CellState.HIDED)
        self.assertTrue(empty_cell.is_eligible_to_reveal_borders())

    def test_MineCell_WillNeverBeEligibleToRevealBorder(self):
        mine_cell = CellObjectFactory.instance(CellObjectType.MINE, row=0, col=0, state=CellState.HIDED)
        self.assertFalse(mine_cell.is_eligible_to_reveal_borders())

    def test_RevealCellResult(self):
        empty_cell = CellObjectFactory.instance(CellObjectType.EMPTY, row=0, col=0, state=CellState.HIDED)
        self.assertEqual(empty_cell.reveal(), RevealCellResult.ALIVE)

        mine_cell = CellObjectFactory.instance(CellObjectType.MINE, row=0, col=0, state=CellState.HIDED)
        self.assertEqual(mine_cell.reveal(), RevealCellResult.LOST)

    def test_RevealCell_HidedCellMustChangeItsStateToRevealed(self):
        empty_cell = CellObjectFactory.instance(CellObjectType.EMPTY, row=0, col=0, state=CellState.HIDED)
        mine_cell = CellObjectFactory.instance(CellObjectType.MINE, row=0, col=0, state=CellState.HIDED)
        empty_cell.reveal()
        mine_cell.reveal()
        self.assertNotIn(CellState.HIDED, [mine_cell.state, empty_cell.state])


class GameBoardTest(TestCase):

    def test_removeAllMines(self):
        board = GameBoard(TOTAL_ROWS, TOTAL_COLS)
        board.add_mine(0, 0)
        board.add_mine(5, 5)
        board.remove_all_mines()

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

    def _game(self, rows=TOTAL_ROWS, cols=TOTAL_COLS, mines=TOTAL_MINES):
        return MinesweeperGame(rows, cols, mines, state=GameState.NEW)

    def _unrevealed_cells(self, game):
        result = []
        for i in range(game.board.rows):
            for j in range(game.board.cols):
                if game.board.cell(i, j).state == CellState.HIDED:
                    result.append((i, j))

        return result

    def _assert_all_cells_revealed(self, game):
        for i in range(game.board.rows):
            for j in range(game.board.cols):
                self.assertEqual(game.board.cell(i, j).state, CellState.REVEALED)

    def test_CreateGame_RaiseExceptionIfAtLeastOneParamIsNotValid(self):
        # invalid rows number
        with self.assertRaises(ValueError):
            _ = MinesweeperGame(-3, 50, 10, state=GameState.NEW)

        # invalid cols number
        with self.assertRaises(ValueError):
            _ = MinesweeperGame(50, -3, 10, state=GameState.NEW)

        # invalid mines number
        with self.assertRaises(ValueError):
            _ = MinesweeperGame(50, 50, -8, state=GameState.NEW)

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
        game = self._game()

        with self.assertRaises(ValueError):
            self.assertEqual(game.reveal(-5, 3), RevealCellResult.INVALID)

    def test_RevealCell_LostTheGameIfMineCellIsRevealed(self):
        game = self._game()
        game.board.remove_all_mines()
        game.board.add_mine(0, 0)
        game.reveal(0, 0)

        self.assertEqual(game.state, GameState.LOST)
        self._assert_all_cells_revealed(game)

    def test_RevealCell_WinTheGameIfAllEmptyCellsWereRevealed(self):
        game = self._game(4, 4, 2)
        game.board.remove_all_mines()
        game.board.add_mine(0, 0)
        game.reveal(0, 2)

        self.assertEqual(game.state, GameState.WIN)
        self._assert_all_cells_revealed(game)

    def test_RevealCell_RevealEmptyCellWillRevealAllEmptyCellsAround(self):
        game = self._game(3, 3, 1)
        game.board.remove_all_mines()
        game.reveal(1, 1)
        self._assert_all_cells_revealed(game)

    def test_RevealCell_RevealCellWithMineInBorderCannotRevealOtherCells(self):
        game = self._game(4, 4, 1)
        game.board.remove_all_mines()
        game.board.add_mine(0, 0)
        game.reveal(0, 1)

        for i in range(4):
            for j in range(4):
                if i == 0 and j == 1:
                    continue

                self.assertEqual(game.cell(i, j).state, CellState.HIDED)

    def test_RevealCell_RevealAllEmptyCellsInsideBorderOfCellsWithNumbers(self):
        """ Cell with numbers are those who at least have one mine in their borders.

         Creating this board for testing

               0 1 2 3 4 5 6 7 8

          0    M 1 0 0 0 0 0 1 M
          1    1 1 0 0 0 0 0 1 1
          2    1 1 0 1 1 1 0 1 1
          3    M 1 0 1 M 1 0 1 M
          4    1 1 0 1 1 1 0 1 1
          5    1 1 0 0 0 0 0 1 1
          6    M 1 0 0 0 0 0 1 M

          Where M is a cell which represents a mine.
        """
        game = self._game(7, 9, 1)
        game.board.remove_all_mines()

        game.set_mine_at(0, 0)
        game.set_mine_at(0, 8)
        game.set_mine_at(3, 4)
        game.set_mine_at(3, 0)
        game.set_mine_at(3, 8)
        game.set_mine_at(6, 0)
        game.set_mine_at(6, 8)
        game.reveal(0, 2)

        self.assertEqual(game.state, GameState.STARTED)

        for i in range(game.board.rows):
            for j in range(game.board.cols):
                cell = game.cell(i, j)
                self.assertEqual(cell.state,
                                 (CellState.HIDED if j in [0, 8] or (i == 3 and j == 4) else CellState.REVEALED))

    def test_RevealCell_RevealAllEmptyCellsWinTheGame_AnotherExample(self):
        """ Creating this board for testing

                   0 1 2 3 4 5 6 7 8

              0    0 0 0 0 0 0 0 0 0
              1    0 0 0 0 0 0 0 0 0
              2    1 1 0 1 1 1 0 1 1
              3    M 1 0 1 M 1 0 1 M
              4    1 1 0 1 1 1 0 1 1
              5    0 0 0 0 0 0 0 0 0
              6    0 0 0 0 0 0 0 0 0
        """

        game = self._game(7, 9, 1)
        game.board.remove_all_mines()
        game.set_mine_at(3, 0)
        game.set_mine_at(3, 4)
        game.set_mine_at(3, 8)
        game.reveal(0, 0)

        self.assertEqual(game.state, GameState.WIN)

