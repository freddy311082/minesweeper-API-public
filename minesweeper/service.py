from hashlib import sha256

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
