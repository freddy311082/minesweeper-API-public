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

    def __init__(self, rows, cols, mines_number, state, started_at=datetime.now(), ended_at=None):
        self.board = GameBoard(rows, cols)
        self._set_random_mines(mines_number)
        self.mines_number = mines_number
        self.state = state
        self.started_at = started_at
        self.ended_at = ended_at

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

    def reveal(self, i, j):
        reveal_result = self.board.cell(i, j).reveal()

        if reveal_result == RevealCellResult.LOST: # mine revealed
            self.state = GameState.LOST
            self.stop_game()

    def stop_game(self):
        self.board.reveal_all()
        self.ended_at = datetime.now()


