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

    def test_EmptyCell_IsEligibleToRevealBorder_FalseIfExistsAtLeastOneMineInTheBorder(self):
        empty_cell = CellObjectFactory.instance(CellObjectType.EMPTY, row=0, col=0, state=CellState.HIDED,
                                                total_mines_in_border=1)
        self.assertFalse(empty_cell.is_eligible_to_reveal_border())

    def test_EmptyCell_IsEligibleToRevealBorder_TrueIfDoesntHaveAtLeastOneMineInTheBorder(self):
        empty_cell = CellObjectFactory.instance(CellObjectType.EMPTY, row=0, col=0, state=CellState.HIDED)
        self.assertTrue(empty_cell.is_eligible_to_reveal_border())

    def test_MineCell_WillNeverBeEligibleToRevealBorder(self):
        mine_cell = CellObjectFactory.instance(CellObjectType.MINE, row=0, col=0, state=CellState.HIDED)
        self.assertFalse(mine_cell.is_eligible_to_reveal_border())
