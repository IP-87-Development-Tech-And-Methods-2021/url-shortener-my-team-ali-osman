import sys

import pytest

print(sys.path)
sys.path[0] += '\\..'

from url_shortener.storage import InMemoryStorage
from url_shortener.logic import Logic
from url_shortener.dto import User
from url_shortener.views import handlers
from pyramid.testing import DummyRequest

def test_logic_fails_to_save_when_key_already_exists():
    storage = InMemoryStorage()
    logic = Logic(storage=storage)
    logic.save_if_not_exists("test", "value 1")
    assert logic.save_if_not_exists("test", "value 2") is False
    assert logic.read_by_key("test") == "value 1"


@pytest.fixture
def logic():
    """ How ok is it to use a shared storage for user tests? Hopefully ok level of ok. """
    return Logic(storage=InMemoryStorage())

@pytest.fixture
def user():
    """ Create user to be used later! """
    return User('test@host.com', 'coolUsername', 'superCoolPassword', 31)


def test_save_user_if_not_exists(logic, user):
    assert logic.save_user('testKey', user) is True
    assert logic.save_user('testKey', user) is False


