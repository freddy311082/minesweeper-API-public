import random

from minesweeper.core.board import GameBoard
from minesweeper.core.cell import CellObjectFactory, CellObjectType


class MinesweeperGame:

    def __init__(self, rows, cols, mines_number):
        self.board = GameBoard(rows, cols)
        self._set_random_mines(mines_number)
        self.mines_number = mines_number

    def _set_random_mines(self, mines_number):
        if 0 <= mines_number <= self.board.total_cells() * 0.4:
            while mines_number > 0:
                row = random.randint(0, self.board.rows - 1)
                col = random.randint(0, self.board.rows - 1)

                if self.board.can_add_mine_to(row, col):
                    self.board.add_mine(row, col)
                    mines_number -= 1
        else:
            raise ValueError('Game cannot be created. Invalid params values.')

    def cell(self, i, j):
        return self.board.cell(i, j)
