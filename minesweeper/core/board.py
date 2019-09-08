import random

from minesweeper.core.cell import CellObjectFactory, CellObjectType


class GameBoard:

    def __init__(self, rows, cols):
        self._validate_params(rows, cols)
        self.cols = cols
        self.rows = rows
        self.mines_number = 0
        self.board = self._create_board()

    def _validate_params(self, rows, cols):
        if rows < 0 or cols < 0:
            raise ValueError('Game cannot be created. Invalid params values.')

    def _create_board(self):
        return [[CellObjectFactory.instance(CellObjectType.EMPTY, row, column) for column in range(self.cols)] for row
                in range(self.rows)]

    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def add_mine(self, row, col):
        if self.is_valid(row, col) and not self.cell(row, col).is_a_mine():
            self.mines_number += 1
            mine_cell = CellObjectFactory.instance(CellObjectType.MINE, row=row, col=col)
            self.board[row][col] = mine_cell
            self.increase_mines_in_border_from(mine_cell)

    def increase_mines_in_border_from(self, cell):
        for i, j in self.all_positions_candidated_to_be_revealed_from(cell):
            self.cell(i, j).register_new_mine_in_border()

    def cell(self, row, col):
        return self.board[row][col] if self.is_valid(row, col) else CellObjectFactory.instance(CellObjectType.INVALID,
                                                                                               row=row, col=col)

    def total_cells(self):
        return self.rows * self.cols

    def can_add_mine_to(self, row, col):
        return self.cell(row, col).can_swap_to_mine()

    def remove_all_mines(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = CellObjectFactory.instance(CellObjectType.EMPTY, i, j)

        self.mines_number = 0

    def reveal_all(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cell(i, j).reveal()

    def all_positions_candidated_to_be_revealed_from(self, cell):
        i = cell.row
        j = cell.col

        return [
            (i - 1, j - 1),
            (i - 1, j),
            (i - 1, j + 1),
            (i, j + 1),
            (i + 1, j + 1),
            (i + 1, j),
            (i + 1, j - 1),
            (i, j - 1),
        ]
