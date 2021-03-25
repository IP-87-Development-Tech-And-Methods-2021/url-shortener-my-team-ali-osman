"""This module contains various examples on how to implement an endpoint"""
import http.client as httplib
from url_shortener.logic import Logic

from pyramid.request import Request
from pyramid.response import Response


def protected_resource_read_example(request: Request) -> Response:
    key = request.matchdict['key']
    logic: Logic = request.registry.logic
    value = logic.get_example(key)

    if value is None:
        return Response(
            status=httplib.NOT_FOUND,
            json_body={
                'status': 'error',
                'reason': 'Resource does not exist'
            },
        )

    return Response(
        status=httplib.OK,
        json_body={
            'key': key,
            'value': value,
        },
    )


def protected_resource_write_example(request: Request) -> Response:
    key = request.matchdict['key']
    value = request.json_body.get('value')

    if value is None:
        return Response(status=httplib.BAD_REQUEST,
                        json_body={
                            'status': 'error',
                            'reason':
                            '`value` was not provided within request',
                        })

    logic: Logic = request.registry.logic
    success = logic.save_example_if_not_exists(key, value)

    if success:
        return Response(
            status=httplib.CREATED,
            headerlist=[('Location',
                         request.registry.base_url + '/resource/' + key)],
        )

    return Response(status=httplib.CONFLICT,
                    json_body={
                        'status': 'error',
                        'reason': 'Resource already exists'
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
