"""This module contains various examples on how to implement an endpoint"""
import http.client as httplib
from url_shortener.logic import Logic

from pyramid.request import Request
from pyramid.response import Response

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

#Old name of the method: protected_resource_write_example
def create_user(request: Request) -> Response:
    logic: Logic = request.registry.logic
    key = logic.get_user_count()
    logic.increase_user_count()
    data = {'email': request.json_body.get('email'), 'passwd': request.json_body.get('passwrd')}

    if data['email'] and data['passwd'] is None:
        return Response(status=httplib.BAD_REQUEST,
                        json_body={
                            'status': 'error',
                            'reason':
                                '`email` or `password` was not provided within request',
                        })

    success = logic.save_example_if_not_exists(key, data)

    if success:
        return Response(
            status=httplib.CREATED,
            headerlist=[('Location',
                         request.registry.base_url + '/resource/' + key)],
            json_body={
                'status': 'User created with this email address.',
                'key': key
            }
        )

    return Response(status=httplib.CONFLICT,
                    json_body={
                        'status': 'error',
                        'reason': 'User already exists'
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
