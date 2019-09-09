from hashlib import sha256

from minesweeper.core.game import MinesweeperGame, GameState
from minesweeper.models import DBManager


class Service:

    def __init__(self, current_user=None):
        self.user = current_user
        self.db_manager = DBManager()

    @staticmethod
    def _encode_password(password):
        return sha256(password.encode('utf-8')).hexdigest()

    def create_user(self, username, password, email):
        self.assert_is_admin()
        return self.db_manager.create_user(username, self._encode_password(password), email)

    def assert_is_admin(self):
        #TODO:  check if current user is the admin
        pass

    def users(self):
        return self.db_manager.users()

    def create_new_game(self, user_id, num_rows, num_cols, num_mines):
        if not user_id:
            raise ValueError('Invalid username.')

        game = MinesweeperGame(num_rows, num_cols, num_mines, GameState.NEW)
        return self.db_manager.create_new_game(user_id, num_rows, num_cols, num_mines, game.board_to_string())

    def games(self, user_id):
        return self.db_manager.user_games(user_id)

