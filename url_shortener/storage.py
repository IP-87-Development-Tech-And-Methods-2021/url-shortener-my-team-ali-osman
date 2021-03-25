from abc import ABC, abstractmethod
from threading import Lock
from typing import Dict, Optional


class Storage(ABC):
    """ Declare base interface for storage """

    @abstractmethod
    def read(self, key: str) -> Optional[str]:
        """ Returns stored value by key """
        raise NotImplementedError

    @abstractmethod
    def write(self, key: str, value: str):
        """ Stores value by key """
        raise NotImplementedError


class InMemoryStorage(Storage):
    """ Simple in-memory implementation of key-value storage.
    Note, how it is inherited from abstract `Storage` class
    and implements all its abstract methods. This is done this way
    in order to make some guarantees regarding class public API
    """

    def __init__(self):
        super().__init__()
        self._write_lock: Lock = Lock()
        self._data: Dict[str, str] = {}

    def read(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def write(self, key: str, value: str):
        with self._write_lock:
            self._data[key] = value
