"""This module contains various examples on how to implement an endpoint"""
import http.client as httplib
import re
import random
import string
from url_shortener.logic import Logic
from url_shortener.dto import User

from pyramid.request import Request
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
domain_name = 'localhost:6543/'


def get_auth_token(request: Request) -> str:
    """ Strips request header to get the Auth id only. """
    return request.headers['Authorization'].replace('Bearer ', '')


# Old name of the method: protected_resource_write_example
def create_user(request: Request) -> Response:
    """ Creates user if all conditions are met.
        CONDITIONS
            - If non-null data entered.
            - If account does not exist.
            - If username does not exits.
            - If username is longer than 4 chars
            - If email address is valid.
        Returns a response.
     """
    logic: Logic = request.registry.logic
    try:
        new_user = User(email=request.json_body.get('email'),
                        username=request.json_body.get('username'),
                        password=request.json_body.get('password'),
                        id=logic.get_user_count())
    except Exception as e:
        print(e)
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'Request body is missing.'
        })

    # Conditions.
    if logic.read_user_by_email(new_user.email):
        return Response(status=httplib.CONFLICT, json_body={
            'status': 'error',
            'description': 'There is already an account with this email.'
        })

    if logic.read_user_by_username(new_user.username):
        return Response(status=httplib.CONFLICT, json_body={
            'status': 'error',
            'description': 'There is already an account with this username.',
        })

    if new_user.email is None or new_user.password is None or new_user.username is None:
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': '`email`, `password` or `username` cannot be null.',
        })

    if len(new_user.username) < 4:
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'Username cannot be less than 3 characters.',
        })
    if not EMAIL_REGEX.match(new_user.email):
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'Please enter a valid email address.',
        })

    logic.add_token(new_user)
    logic.increase_user_count()

    success = logic.save_user(str(new_user.id), new_user)

    if success:
        return Response(
            status=httplib.CREATED, json_body={
                'status': 'User created with this email address.',
                'id': new_user.id,
                'token-type': 'Bearer',
                'token': new_user.token
            }
        )

    return Response(status=httplib.INTERNAL_SERVER_ERROR , json_body={
        'status': 'error',
        'description': 'Unexpected error occurred.'
    })


def login_user(request: Request) -> Response:
    """
        Logs in the user.
        CONDITIONS:
            - If username and password entered.
            - If username and password are non-null.
            - If username is longer than 4 chars.
            - If user is not logged in already.
        Returns a response.
    """
    logic: Logic = request.registry.logic
    try:
        username_entered = request.json_body.get('username')
        password_entered = request.json_body.get('password')
    except Exception as e:
        print(e)
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'Request body is missing.'
        })

    # Conditions.
    if username_entered is None and password_entered is None:
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': '`username` or `password` cannot be null.',
        })
    if len(username_entered) < 4:
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'Username cannot be less than 4 characters.',
        })
    user = logic.read_user_by_username(username_entered)

    # Check if user is already logged in
    if any(user.username == k.username for k in logic.get_tokens()):
        return Response(
            status=httplib.CONFLICT, json_body={
                'status': 'error',
                'description': 'You are already logged in!'
            }
        )

    if user is not None:
        logic.add_token(user)
        return Response(
            status=httplib.CREATED, json_body={
                'status': 'success',
                'description': f'Welcome, {user.username}. Please use your token for operations.',
                'id': user.id,
                'token-type': 'Bearer',
                'token': user.token
            }
        )
    else:
        return Response(
            status=httplib.BAD_REQUEST, json_body={
                'status': 'error',
                'description': 'User was not found.'
            }
        )


def logout_user(request: Request) -> Response:

    """Logs out user."""

    logic: Logic = request.registry.logic

    if logic.remove_token(get_auth_token(request)):

        return Response(status=httplib.OK, json_body={
            'status': 'Success',
            'description': 'Successfully logged out.'
        })
    else:
        return Response(status=httplib.CONFLICT, json_body={
            'status': 'error',
            'description': 'Smth went wrong.'
        })


def redirect_longlink(request: Request):
    """ Redirects if conditions are met.
        CONDITIONS:
            - If data entered is non-null
            - If key exists.
            - If key is valid.
        Returns HTTPFound
    """

    logic: Logic = request.registry.logic
    try:
        id = request.matchdict['id']
    except Exception as e:
        print(e)
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'Request body is missing.'
        })

    try:
        long_link = logic.read_by_key(id)
    except Exception as e:
        print(e)
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'Key does not exist.'
        })

    if id is None or long_link is None:
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'Incorrect key.'
        })

    return HTTPFound(location=long_link)


def create_shortlink(request: Request) -> Response:
    """ Creates a shortlink id, by using id if provided or generating 4 char random string."""
    logic: Logic = request.registry.logic

    try:
        url_provided = request.json_body.get('url')
        id_provided = request.json_body.get('id')
    except Exception as e:
        print(e)
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'Request body is missing.'
        })

    if url_provided is None:
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'URL must be provided.'
        })

    # If custom id is not provided, or this id already exists, we give an random one.
    while id_provided is None or logic.read_by_key(id_provided) is not None:
        id_provided = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(4))

    # People shouldn't overwrite user id's so we'll block it.
    if any(c.isdigit() for c in id_provided):
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'Numbers in id is not allowed.'
        })

    # URL check if it's valid. (stolen from django url validation regex)
    regex_check = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not re.match(regex_check, url_provided.lower()) is not None:
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'URL is incorrect.'
        })

    success = logic.save_if_not_exists(id_provided, url_provided.lower())

    # If saving the shortlink succeeds, save this info to user.
    if success:
        new_user = logic.find_user_by_token(get_auth_token(request))
        new_user.urls.append(id_provided)
        logic.save_user(str(new_user.id), new_user)
        return Response(status=httplib.OK, json_body={
            'status': 'success',
            'description': 'Successfully created short url.',
            'id': id_provided,
            'shortened_link': domain_name + id_provided
        })

    return Response(status=httplib.INTERNAL_SERVER_ERROR,
                    json_body={
                        'status': 'error',
                        'description': 'An unexpected error occurred.'
                    })


def list_links_for_user(request: Request) -> Response:
    logic: Logic = request.registry.logic

    user = logic.find_user_by_token(get_auth_token(request))
    print(user.urls)

    k = {}
    for m in user.urls:
        k[domain_name + m] = logic.read_by_key(m)

    return Response(status=httplib.OK,
                    json_body={
                        'status': 'successful',
                        'description': 'Fetched all data.',
                        'found_data': k
                    })


def delete_shortlink(request: Request) -> Response:
    logic: Logic = request.registry.logic

    try:
        id_provided = request.json_body.get('id')
    except Exception as e:
        print(e)
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'Request body is missing.'
        })

    user = logic.find_user_by_token(get_auth_token(request))

    if not (id_provided in user.urls):
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': "Couldn't find provided id listed."
        })

    user.urls.remove(id_provided)

    logic.save_user(str(user.id), user)
    logic.remove_value_by_key(id_provided)

    return Response(status=httplib.OK,
                    json_body={
                        'status': 'success',
                        'description': f'Key {id_provided} removed successfully.'
                    })


def public_resource_example(request: Request) -> Response:
    return Response(status=httplib.OK, json_body={'available_for': 'everyone'})


def notfound(request: Request) -> Response:
    return Response(status=httplib.NOT_FOUND, json_body={
        'status': 'error',
        'description': 'Resource does not exist'
    })


def forbidden(request: Request) -> Response:
    return Response(status=httplib.FORBIDDEN, json_body={
        'status': 'error',
        'description': 'Access denied'
    })
