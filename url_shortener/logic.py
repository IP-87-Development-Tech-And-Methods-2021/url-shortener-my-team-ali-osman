from threading import Lock
from typing import Optional
import random
import string
import re

from url_shortener.storage import Storage
from url_shortener.dto import User
import logging

log = logging.getLogger(__name__)


class Logic:
    """This class implements application logic"""

    def __init__(self, storage: Storage):
        """ Creating an instance of our logic. Pay attention that storage is not created within the logic, but
        passed as a parameter from outside. This is called Dependency Injection.
        """
        log.info('Logic is initilized.')
        super().__init__()
        self._storage: Storage = storage
        self._check_and_write_lock: Lock = Lock()
        self._storage.write('userCount', 0)
        log.info('userCount is set to 0')
        self._storage.write('authTokens', {})
        log.info("authTokens is set to {}.")

    # Auth methods:
    def get_tokens(self) -> {}:
        """ Returns all the users that are logged in. """
        return self._storage.read('authTokens')

    def add_token(self, token: str, username: str):
        """ Appends user to the logged in users."""
        token_list = self.get_tokens()
        token_list[token] = username
        self._storage.write('authTokens', token_list)
        log.info('User saved')

    def remove_token(self, token: str) -> bool:
        """ Removes user from logged in users list. """
        token_list = self.get_tokens()
        if token_list[token] is not None:
            # token_list[token] = None
            token_list.pop(token, None)
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
        """ If saves user successfully returns True. """
        with self._check_and_write_lock:
            existing = self._storage.read(key)
            if existing is not None:
                return False

            self._storage.write(key, value)
            return True

    def find_user_by_token(self, token: str) -> Optional[User]:
        all_tokens = self.get_tokens()
        if token in all_tokens.keys():
            return self.read_user_by_username(all_tokens[token])
        return None

    # old name of the method: get_example
    def read_by_key(self, key: str) -> Optional[str]:
        """Retrieves data from storage by key"""
        return self._storage.read(key)

    def save_if_not_exists(self, key: str, value: str) -> bool:
        """ Tries to save value at given key.
        Fails if key already has value in the storage.
        Returns True if saving value was successful, otherwise False
        """
        # Acquire lock, so that we do not get ourselves into the data race
        with self._check_and_write_lock:
            existing = self._storage.read(key)
            if existing is not None:
                return False

            self._storage.write(key, value)
            return True

    def remove_value_by_key(self, key: str):
        self._storage.write(key, None)

    length_of_shortlink = 4

    def give_random_string(self, id: str) -> str:
        """ Returns an random string with prechecks. If inputted data is invalid it'll be replaced. """
        # There are ((62 ** length_of_shortlink) - (10 ** length_of_shortlink)) amount of options. 62 ** 4 = 14_774_336
        options = string.ascii_uppercase + string.ascii_lowercase + string.digits
        counter = 0
        # Only number id's are unacceptable. Because we keep users with ids.

        while id is None or self.read_by_key(id) is not None or not any(char.isalpha() for char in id):
            counter += 1
            if counter > 1_000_000:
                self.length_of_shortlink += 1
            id = ''.join(random.choice(options) for _ in range(self.length_of_shortlink))
        return id

    def is_url_valid(self, url: str) -> bool:
        """ URL check if it's valid. (stolen from django url validation regex) """
        regex_check = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return not re.match(regex_check, url.lower()) is not None

    def is_email_valid(self, email: str) -> bool:
        return re.compile(r"[^@]+@[^@]+\.[^@]+").match(email) is not None
