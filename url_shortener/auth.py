"""
This module holds all authentication/authorization related code.
You probably do not need to mess with it
"""
from typing import Optional

from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.request import Request
from pyramid.authorization import (ALL_PERMISSIONS, Allow, Authenticated, Deny,
                                   Everyone)
from zope.interface import implementer

from url_shortener.dto import User


@implementer(IAuthenticationPolicy)
class TokenAuthenticationPolicy(CallbackAuthenticationPolicy):
    _TOKEN_PREFIX = 'Bearer '
    _TOKEN_PREFIX_LOWERCASE = _TOKEN_PREFIX.lower()

    def identity(self, request: Request) -> Optional[User]:
        auth_header: str = request.headers.get('Authorization')
        if auth_header is None:
            return None

        if not auth_header.lower().startswith(self._TOKEN_PREFIX_LOWERCASE):
            return None

        token = auth_header[len(self._TOKEN_PREFIX):]
        authenticated_user = request.registry.logic.find_user_by_token(token)
        return authenticated_user

    def authenticated_userid(self, request: Request):
        identity = self.identity(request)
        if identity is not None:
            return identity.email
        return None

    def effective_principals(self, request: Request):
        principals = [Everyone]
        identity = self.identity(request)
        if identity is not None:
            principals += [Authenticated, identity.email]
        return principals


class Protected:
    __acl__ = (
        (Allow, Authenticated, ALL_PERMISSIONS),
        (Deny, Everyone, ALL_PERMISSIONS),
    )


PROTECTED_CONTEXT = Protected()


def protected(request):
    return PROTECTED_CONTEXT
