"""This module contains various examples on how to implement an endpoint"""
import http.client as httplib
import re
from url_shortener.logic import Logic
from url_shortener.dto import User

from pyramid.request import Request
from pyramid.response import Response

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


# Old name of the method: protected_resource_read_example
def read_user(request: Request) -> Response:
    key = request.matchdict['key']
    logic: Logic = request.registry.logic
    data = {'email': logic.read_by_key(key)['email'], 'passwd': logic.read_by_key(key)['passwd']}

    if data['email'] is None:
        return Response(
            status=httplib.NOT_FOUND,
            json_body={
                'status': 'error',
                'reason': 'User does not exist'
            },
        )

    return Response(
        status=httplib.OK,
        json_body={
            'key': key,
            'email': data['email'],
            'password': data['passwd'],
        },
    )


# Old name of the method: protected_resource_write_example
def create_user(request: Request) -> Response:

    logic: Logic = request.registry.logic

    new_user = User(email=request.json_body.get('email'),
                   username=request.json_body.get('username'),
                   password=request.json_body.get('password'),
                   id=logic.get_user_count(),
                   token=str(hash(request.json_body.get('username'))))
    # Conditions.
    # TODO: check for duplication of username or email.
    if new_user.email and new_user.password and new_user.username is None:
        return Response(status=httplib.BAD_REQUEST,
                        json_body={
                            'status': 'error',
                            'reason':
                                '`email`, `password` or `username` cannot be null.',
                        })
    if len(new_user.username) < 4:
        return Response(status=httplib.BAD_REQUEST,
                        json_body={
                            'status': 'error',
                            'reason':
                                'Username cannot be less than 3 characters.',
                        })
    if not EMAIL_REGEX.match(new_user.email):
        return Response(status=httplib.BAD_REQUEST,
                        json_body={
                            'status': 'error',
                            'reason':
                                'Please enter a valid email address.',
                        })

    logic.add_token(new_user)
    logic.increase_user_count()

    success = logic.save_user(str(new_user.id), new_user)

    if success:
        return Response(
            status=httplib.CREATED,
            # headerlist=[('Location', request.registry.base_url + '/resource/' + key)], # Do we need it?
            json_body={
                'status': 'User created with this email address.',
                'id': new_user.id,
                'token-type': 'Bearer',
                'token': new_user.token
            }
        )

    return Response(status=httplib.CONFLICT,
                    json_body={
                        'status': 'error',
                        'reason': 'User already exists'
                    })


def login_user(request: Request) -> Response:
    logic: Logic = request.registry.logic
    username_entered = request.json_body.get('username')
    password_entered = request.json_body.get('password')

    # Conditions.
    # TODO: check if user is already logged in
    if username_entered and password_entered is None:
        return Response(status=httplib.BAD_REQUEST,
                        json_body={
                            'status': 'error',
                            'reason':
                                '`username` or `password` cannot be null.',
                        })
    if len(username_entered) < 4:
        return Response(status=httplib.BAD_REQUEST,
                        json_body={
                            'status': 'error',
                            'reason':
                                'Username cannot be less than 3 characters.',
                        })

    search_result = logic.read_user_by_username(username_entered)
    if search_result is not None:
        logic.add_token(search_result)
        return Response(
            status=httplib.CREATED,
            # headerlist=[('Location', request.registry.base_url + '/resource/' + key)], # Do we need it?
            json_body={
                'status': 'success',
                'description': f'Welcome, {search_result.username}. Please use your token for operations.',
                'id': search_result.id,
                'token-type': 'Bearer',
                'token': search_result.token
            }
        )
    else:
        return Response(
            status=httplib.BAD_REQUEST,
            # headerlist=[('Location', request.registry.base_url + '/resource/' + key)], # Do we need it?
            json_body={
                'status': 'error',
                'description': 'User was not found.'
            }
        )


def logout_user(request: Request) -> Response:
    logic: Logic = request.registry.logic

    print(request.headers['Authorization'].replace('Bearer ', ''))
    if logic.remove_token(request.headers['Authorization'].replace('Bearer ', '')):

        return Response(status=httplib.CONFLICT,
                        json_body={
                            'status': 'smth',
                            'reason': 'yay'
                        })
    else:
        return Response(status=httplib.CONFLICT,
                        json_body={
                            'status': 'error',
                            'reason': 'Smth went wrong.'
                        })


def public_resource_example(request: Request) -> Response:
    return Response(status=httplib.OK, json_body={'available_for': 'everyone'})


def notfound(request: Request) -> Response:
    return Response(status=httplib.NOT_FOUND, json_body={
        'status': 'error',
        'reason': 'Resource does not exist'
    })


def forbidden(request: Request) -> Response:
    return Response(status=httplib.FORBIDDEN, json_body={
        'status': 'error',
        'reason': 'Access denied'
    })
