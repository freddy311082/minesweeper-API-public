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


class Cell(ABC):
    CELL_OBJECT_TYPE = CellObjectType.INVALID

    @classmethod
    def is_type(cls, obj_type):
        return cls.CELL_OBJECT_TYPE == obj_type

    def __init__(self, row, col, state=CellState.HIDED):
        self.row = row
        self.col = col
        self.state = state

    def can_be_revealed(self):
        return self.state == CellState.HIDED


class EmptyCell(Cell):
    CELL_OBJECT_TYPE = CellObjectType.EMPTY


class MineCell(Cell):
    CELL_OBJECT_TYPE = CellObjectType.MINE


class InvalidCell(Cell):
    """ Null Pattern implementation. """

    def can_be_revealed(self):
        return False


class CellObjectFactory:
    @staticmethod
    def instance(obj_type, *args, **kwargs):
        return Factory.instance(obj_type, Cell, InvalidCell, *args, **kwargs)
