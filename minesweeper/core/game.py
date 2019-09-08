

class MinesweeperGame:

    def __init__(self, rows, cols, mines_number):
        self._validate_params(rows, cols, mines_number)
        self.cols = cols
        self.rows = rows
        self.mines_number = mines_number

    def _validate_params(self, rows, cols, mines_number):
        if rows < 0 or cols < 0 or mines_number < 0 or mines_number < rows*cols * 0.4:
            raise ValueError('Game cannot be created. Invalid params values.')


