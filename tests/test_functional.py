import sys
print(sys.path)
sys.path[0] += '\\..'

from url_shortener.storage import InMemoryStorage
from url_shortener.logic import Logic

def test_public(testapp):
    res = testapp.get('/public', status=200)
    assert 'available_for' in res.json_body


def test_notfound(testapp):
    # Returns 400 Bad request. Because redirect_longlink. Because http://host/shortLinkID will forward to the long link.
    res = testapp.get('/badurl', status=400)
    assert res.status_code == 400


def test_notfound_for_real(testapp):
    # Returns 400 Bad request. Because redirect_longlink. Because http://host/shortLinkID will forward to the long link.
    res = testapp.get('/really/badurl', status=404)
    assert res.status_code == 404


def test_logic_is_url_valid():
    storage = InMemoryStorage()
    logic = Logic(storage=storage)
    assert logic.is_url_valid('') is False
    assert logic.is_url_valid('something') is False
    assert logic.is_url_valid('something.com') is False
    assert logic.is_url_valid('http/something.com') is False
    assert logic.is_url_valid('http://smth') is False
    assert logic.is_url_valid('http://smth.com') is True
    assert logic.is_url_valid('http://localhost:6543') is True
    assert logic.is_url_valid('http://smth.com/somethingCool') is True

def test_logic_is_email_valid():
    storage = InMemoryStorage()
    logic = Logic(storage=storage)
    assert logic.is_email_valid('') is False
    assert logic.is_email_valid('smth') is False
    assert logic.is_email_valid('smth@smth') is False
    assert logic.is_email_valid('smth@smth@smth') is False
    assert logic.is_email_valid('smth@smth.smth') is True
    assert logic.is_email_valid('smth.smth@smth.smth') is True
