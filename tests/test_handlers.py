import sys
import pytest
print(sys.path)
sys.path[0] += '\\..'

from url_shortener.views import handlers
from pyramid.testing import DummyRequest


def test_create_user(app_request):
    res = handlers.create_user(app_request)
    assert res.status_code == 400, "It's a bad req. 400"

    res = handlers.create_user(
        DummyRequest(
            json_body={"email": "kaankaray99@gmail.com", "username": "kaan", "password": "smth"},
            method='POST'
        )
    )
    assert res.status_code == 201

    res = handlers.create_user(
        DummyRequest(
            json_body={"email": "kaankaray99@gmail.com", "username": "kaan", "password": "smth"},
            method='POST'
        )
    )
    assert res.status_code == 409, f"Should've return 409, this acc already exists.{res.json_body}"

    res = handlers.create_user(
        DummyRequest(
            json_body={},
            method='POST'
        )
    )
    assert res.status_code == 400, f"There is no body. Should've been 400. {res.json_body}"

    res = handlers.create_user(
        DummyRequest(
            json_body={"email": "test@test.com", "password": "smth"},
            method='POST'
        )
    )
    assert res.status_code == 400, f"There is no username. {res.json_body}"

    res = handlers.create_user(
        DummyRequest(
            json_body={"email": "test@test.com", "username": "testttt"},
            method='POST'
        )
    )
    assert res.status_code == 400, f"There is no password{res.json_body}"

    res = handlers.create_user(
        DummyRequest(
            json_body={"username": "testttt", "password": "smth"},
            method='POST'
        )
    )
    assert res.status_code == 400, f"There is no email address inputted{res.json_body}"

    res = handlers.create_user(
        DummyRequest(
            json_body={"email": "test@test.com", "username": "123", "password": "smth"},
            method='POST'
        )
    )
    assert res.status_code == 400, f"Username should be longer than 3 chars. 400 {res.json_body}"

    res = handlers.create_user(
        DummyRequest(
            json_body={"email": "invalid Email Address", "username": "testttt", "password": "smth"},
            method='POST'
        )
    )
    assert res.status_code == 400, f"An invalid email address 400 {res.json_body}"

# TODO: Login, logout.
#
# def test_login_user(app_request):
#     res = handlers.create_user(
#         DummyRequest(
#             json_body={"email": "test@test.com", "username": "test", "password": "smth"},
#             method='POST'
#         )
#     )
#     print(res.json_body)
#     req = DummyRequest().headers['Authorization'] = 'Bearer ' + res.json_body['token']
#
#
#     res = handlers.create_user(req)
#     assert res.status_code == 400, "It's a bad req. 400"
#
#
#     # Gotta logout first, need the bearer key for it getting that is gonna be a pain
#
#     res = handlers.login_user(
#         DummyRequest(
#             json_body={"username": "test", "password": "smth"},
#             method='POST'
#         )
#     )
#     assert res.status_code == 200, f"{res.json_body}"
#
#     res = handlers.login_user(
#         DummyRequest(
#             json_body={},
#             method='POST'
#         )
#     )
#     assert res.status_code == 400, f"There is no body. Should've been 400. {res.json_body}"
#
#     res = handlers.login_user(
#         DummyRequest(
#             json_body={"password": "smth"},
#             method='POST'
#         )
#     )
#     assert res.status_code == 400, f"There is no username. {res.json_body}"
#
#     res = handlers.login_user(
#         DummyRequest(
#             json_body={"username": "test"},
#             method='POST'
#         )
#     )
#     assert res.status_code == 400, f"There is no password{res.json_body}"
#
#     res = handlers.login_user(
#         DummyRequest(
#             json_body={"username": "123", "password": "smth"},
#             method='POST'
#         )
#     )
#     assert res.status_code == 400, f"Username should be longer than 3 chars. 400 {res.json_body}"
