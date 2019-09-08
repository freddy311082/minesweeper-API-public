from django.test import TestCase

from minesweeper.core.cell import CellObjectFactory, CellObjectType, CellState


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
