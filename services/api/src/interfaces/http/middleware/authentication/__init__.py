from flask import request, g

from interfaces.http.config import Config
from interfaces.http.middleware.authentication import (
    basic_authentication as basic_auth,
    access,
)
from interfaces.http.validation import Validator


class AuthenticationMiddleware:
    def __init__(
        self,
        basic_authentication: basic_auth.Middleware,
        access: access.Middleware,
    ):
        self._basic_authentication = basic_authentication
        self._access = access

    @property
    def basic_authentication(self) -> basic_auth.Middleware:
        return self._basic_authentication

    @property
    def required(self) -> access.Middleware:
        return self._access


def create_middleware(
    config: Config, validator: Validator
) -> AuthenticationMiddleware:
    basic_authentication = basic_auth.Middleware(config, validator)
    _access = access.Middleware()
    middleware = AuthenticationMiddleware(
        basic_authentication=basic_authentication,
        access=_access,
    )
    return middleware
