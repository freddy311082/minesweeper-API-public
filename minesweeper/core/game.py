import random
from enum import Enum
from minesweeper.core.board import GameBoard
from datetime import datetime

from minesweeper.core.cell import RevealCellResult


class GameState(Enum):
    NEW = 0
    STARTED = 1
    PAUSE = 2
    WIN = 3
    LOST = 4


class MinesweeperGame:

    def __init__(self, rows, cols, mines_number, state, started_at=datetime.now(), ended_at=None,
                 total_cells_revealed=0):
        self.board = GameBoard(rows, cols)
        self._set_random_mines(mines_number)
        self.state = state
        self.started_at = started_at
        self.ended_at = ended_at
        self.total_cells_revealed = total_cells_revealed

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

    def set_mine_at(self, i, j):
        self.board.add_mine(i, j)

    def cell(self, i, j):
        return self.board.cell(i, j)

    def reveal(self, i, j):
        if self.state == GameState.NEW:
            self.state = GameState.STARTED

        cell = self.cell(i, j)
        reveal_result = cell.reveal()
        {
            RevealCellResult.LOST: self.notify_lost,
            RevealCellResult.INVALID: self.notify_invalid_cell,
            RevealCellResult.ALIVE: self.empty_cell_revealed
        }[reveal_result](cell)

    def end_game(self):
        self.board.reveal_all()
        self.ended_at = datetime.now()

    def notify_lost(self, cell):
        self.state = GameState.LOST
        self.end_game()

    def notify_invalid_cell(self, cell):
        raise ValueError("Cell ({},{}) cannot be revealed as it's not valid".format(cell.row, cell.col))

    def notify_win(self):
        self.end_game()
        self.state = GameState.WIN

    def empty_cell_revealed(self, cell):
        self.register_empty_cell_revealed()
        self.reveal_borders(cell)
        self.update_game_state_if_needed()

    def register_empty_cell_revealed(self):
        self.total_cells_revealed += 1

    def were_all_empty_cells_revealed(self):
        return self.total_cells_revealed == self.board.total_cells() - self.board.mines_number

    def update_game_state_if_needed(self):
        if self.were_all_empty_cells_revealed():
            self.notify_win()

    def reveal_borders(self, cell):
        if cell.is_eligible_to_reveal_borders():
            for row, col in self.board.all_positions_candidated_to_be_revealed_from(cell):
                cell_to_reveal = self.board.cell(row, col)

                if cell_to_reveal.can_be_revealed() and not cell_to_reveal.is_a_mine():
                    cell_to_reveal.reveal()
                    self.register_empty_cell_revealed()
                    self.reveal_borders(cell_to_reveal)
