"""This module contains various examples on how to implement an endpoint"""
import http.client as httplib
from url_shortener.logic import Logic

from pyramid.request import Request
from pyramid.response import Response


def protected_resource_read_example(request: Request) -> Response:
    key = request.matchdict['key']
    logic: Logic = request.registry.logic
    email = logic.get_example(key)
    passwrd = logic.get_example(key)

    if email is None:
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
            'email': email,
            'password': passwrd,
        },
    )


def protected_resource_write_example(request: Request) -> Response:
    key = request.matchdict['key']
    email = request.json_body.get('email')
    passwrd = request.json_body.get('passwrd')

    if email and passwrd is None:
        return Response(status=httplib.BAD_REQUEST,
                        json_body={
                            'status': 'error',
                            'reason':
                            '`email` or `password` was not provided within request',
                        })

    logic: Logic = request.registry.logic
    success = logic.save_example_if_not_exists(key, email, passwrd,)

    if success:
        return Response(
            status=httplib.CREATED,
            headerlist=[('Location',
                         request.registry.base_url + '/resource/' + key)],
            json_body={
                'status': 'User'
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
