from threading import Lock
from typing import Optional

from url_shortener.storage import Storage
from url_shortener.dto import User


class Logic:
    """This class implements application logic"""

    def __init__(self, storage: Storage):
        """ Creating an instance of our logic. Pay attention that storage is not created within the logic, but
        passed as a parameter from outside. This is called Dependency Injection.
        """
        print("Logic is initilized.")
        super().__init__()
        self._storage: Storage = storage
        self._check_and_write_lock: Lock = Lock()
        self._storage.write('userCount', 0)
        print("userCount is set to 0.")
        self._storage.write('authTokens', [])
        print("authTokens is set to [].")

    # Auth methods:
    def get_tokens(self) -> Optional[User]:
        return self._storage.read('authTokens')

    def add_token(self, token: User):
        token_list = self.get_tokens()
        token_list.append(token)
        self._storage.write('authTokens', token_list)
        print(self.get_tokens())

    def remove_token(self, token: str) -> bool:
        token_list = self.get_tokens()
        for k in token_list:
            if k.token == token:
                token_list.remove(k)
                self._storage.write('authTokens', token_list)
                return True
        return False

    # User counter methods:
    def get_user_count(self) -> int:
        return self._storage.read('userCount')

    def set_user_count(self, value: int) -> int:
        self._storage.write('userCount', value)
        return self.get_user_count()

    def increase_user_count(self) -> int:
        self._storage.write('userCount', self._storage.read('userCount') + 1)
        return self.get_user_count()

    # User read-write
    def read_user_with_id(self, key: int) -> Optional[User]:
        return self._storage.read(key)

    def read_user_by_email(self, email: str) -> Optional[User]:
        for m in range(self.get_user_count()):
            k = self.read_user_with_id(str(m))
            if k.email == email:
                return k
        return None

    def read_user_by_username(self, username: str) -> Optional[User]:
        for m in range(self.get_user_count()):
            k = self.read_user_with_id(str(m))
            if k.username == username:
                return k
        return None

    def save_user(self, key: str, value: User) -> bool:
        with self._check_and_write_lock:
            existing = self._storage.read(key)
            if existing is not None:
                return False

            self._storage.write(key, value)
            return True

    def find_user_by_token(self, token: str) -> Optional[User]:
        for k in self.get_tokens():
            if k.token == token:
                return k
        return None



    # Old deprecated methods
    # old name of the method: get_example
    # def read_by_key(self, key: str) -> Optional[str]:
    #     """Retrieves data from storage by key"""
    #     return self._storage.read(key)
    #
    # def save_example_if_not_exists(self, key: str, value: str) -> bool:
    #     """ Tries to save value at given key.
    #     Fails if key already has value in the storage.
    #     Returns True if saving value was successful, otherwise False
    #     """
    #     # Acquire lock, so that we do not get ourselves into the data race
    #     with self._check_and_write_lock:
    #         existing = self._storage.read(key)
    #         if existing is not None:
    #             return False
    #
    #         self._storage.write(key, value)
    #         return True
