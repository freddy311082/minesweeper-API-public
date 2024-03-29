from enum import Enum
from abc import ABC, abstractmethod

from minesweeper.core.utils import Factory


class CellObjectType(Enum):
    EMPTY = 0
    MINE = 1
    INVALID = 2


class CellState(Enum):
    HIDED = 0
    REVEALED = 1


class RevealCellResult(Enum):
    ALIVE = 0
    LOST = 1
    INVALID = 2


class Cell(ABC):
    CELL_OBJECT_TYPE = CellObjectType.INVALID

    @classmethod
    def is_type(cls, obj_type):
        return cls.CELL_OBJECT_TYPE == obj_type

    def __init__(self, row, col, state=CellState.HIDED, flagged=False):
        self.row = row
        self.col = col
        self.state = state
        self.flagged = flagged

    def can_be_revealed(self):
        return self.state == CellState.HIDED

    @abstractmethod
    def is_eligible_to_reveal_borders(self):
        pass

    def can_swap_to_mine(self):
        return False

    def is_a_mine(self):
        return False

    def reveal(self):
        self.state = CellState.REVEALED
        return self._reveal_result()

    @abstractmethod
    def _reveal_result(self):
        pass

    @abstractmethod
    def register_new_mine_in_border(self):
        pass


class EmptyCell(Cell):
    CELL_OBJECT_TYPE = CellObjectType.EMPTY

    def __init__(self, row, col, state=CellState.HIDED, flagged=False, total_mines_in_border=0):
        super(EmptyCell, self).__init__(row, col, state, flagged)
        self.total_mines_in_border = total_mines_in_border

    def is_eligible_to_reveal_borders(self):
        return self.total_mines_in_border == 0 and not self.flagged

    def _reveal_result(self):
        return RevealCellResult.ALIVE

    def can_swap_to_mine(self):
        return True

    def register_new_mine_in_border(self):
        self.total_mines_in_border += 1

    def __str__(self):
        return str(self.total_mines_in_border)


class MineCell(Cell):
    CELL_OBJECT_TYPE = CellObjectType.MINE

    def is_eligible_to_reveal_borders(self):
        return False

    def reveal(self):
        self.state = CellState.REVEALED
        return RevealCellResult.LOST

    def is_a_mine(self):
        return True

    def _reveal_result(self):
        return RevealCellResult.LOST

    def register_new_mine_in_border(self):
        pass

    def __str__(self):
        return 'M'


class InvalidCell(Cell):
    """ Null Pattern implementation. """

    def can_be_revealed(self):
        return False

    def is_eligible_to_reveal_borders(self):
        return False

    def _reveal_result(self):
        return RevealCellResult.INVALID

    def register_new_mine_in_border(self):
        pass

    def __str__(self):
        return 'I'


class CellObjectFactory:
    @staticmethod
    def instance(obj_type, *args, **kwargs):
        return Factory.instance(obj_type, Cell, InvalidCell, *args, **kwargs)
