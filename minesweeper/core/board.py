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
        return [[CellObjectFactory.instance(CellObjectType.EMPTY, row, column) for row in range(self.rows)] for column
                in range(self.cols)]

    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def add_mine(self, row, col):
        if self.is_valid(row, col):
            self.mines_number += 1
            self.board[row][col] = CellObjectFactory.instance(CellObjectType.MINE, row=row, col=col)

    def cell(self, row, col):
        return self.board[row][col] if self.is_valid(row, col) else CellObjectFactory.instance(CellObjectType.INVALID,
                                                                                               row=row, col=col)

    def total_cells(self):
        return self.rows * self.cols

    def can_add_mine_to(self, row, col):
        return self.cell(row, col).can_swap_to_mine()

    def remove_mines(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cell(i, j).is_a_mine():
                    self.board[i][j] = CellObjectFactory.instance(CellObjectType.EMPTY, i, j)

        self.mines_number = 0

    def reveal_all(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cell(i, j).reveal()
