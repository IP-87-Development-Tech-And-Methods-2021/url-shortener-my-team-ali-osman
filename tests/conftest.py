import os
from pyramid.paster import get_appsettings
from pyramid.scripting import prepare
from pyramid.testing import DummyRequest, testConfig
import pytest
import webtest

from url_shortener.main import make_app
from url_shortener.config import Config


@pytest.fixture(scope='session')
def app():
    config = Config(base_url='http://127.0.0.1:6543', port=6543)
    return make_app(config)


@pytest.fixture
def testapp(app):
    testapp = webtest.TestApp(app)
    return testapp


@pytest.fixture
def app_request(app):
    """
    A real request.
    This request is almost identical to a real request but it has some
    drawbacks in tests as it's harder to mock data and is heavier.
    """
    with prepare(registry=app.registry) as env:
        request = env['request']
        request.host = 'example.com'
        yield request


@pytest.fixture
def dummy_request():
    """
    A lightweight dummy request.
    This request is ultra-lightweight and should be used only when the request
    itself is not a large focus in the call-stack.  It is much easier to mock
    and control side-effects using this object, however:
    - It does not have request extensions applied.
    - Threadlocals are not properly pushed.
    """
    request = DummyRequest()
    request.host = 'example.com'

    return request
