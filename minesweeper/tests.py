from django.test import TestCase

from minesweeper.core.cell import CellObjectFactory, CellObjectType, CellState


class CellTests(TestCase):

    def test_EmptyCell_CanBeRevealed_RevealedCellsCannotBeRevealed(self):
        cell = CellObjectFactory.instance(CellObjectType.EMPTY, row=0, col=0, state=CellState.REVEALED)
        self.assertFalse(cell.can_be_revealed())
