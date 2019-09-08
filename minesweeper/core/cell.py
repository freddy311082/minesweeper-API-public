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
    def is_eligible_to_reveal_border(self):
        pass

    @abstractmethod
    def reveal(self):
        pass


class EmptyCell(Cell):
    CELL_OBJECT_TYPE = CellObjectType.EMPTY

    def __init__(self, row, col, state=CellState.HIDED, flagged=False, total_mines_in_border=0):
        super(EmptyCell, self).__init__(row, col, state, flagged)
        self.total_mines_in_border = total_mines_in_border

    def is_eligible_to_reveal_border(self):
        return self.total_mines_in_border == 0 and not self.flagged

    def reveal(self):
        self.state = CellState.REVEALED
        return RevealCellResult.ALIVE


class MineCell(Cell):
    CELL_OBJECT_TYPE = CellObjectType.MINE

    def is_eligible_to_reveal_border(self):
        return False

    def reveal(self):
        self.state = CellState.REVEALED
        return RevealCellResult.LOST


class InvalidCell(Cell):
    """ Null Pattern implementation. """

    def can_be_revealed(self):
        return False

    def is_eligible_to_reveal_border(self):
        return False

    def reveal(self):
        return RevealCellResult.ALIVE


class CellObjectFactory:
    @staticmethod
    def instance(obj_type, *args, **kwargs):
        return Factory.instance(obj_type, Cell, InvalidCell, *args, **kwargs)
