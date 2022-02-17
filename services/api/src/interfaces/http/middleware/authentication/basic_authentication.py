import functools
from typing import Any, Tuple, Dict

from flask import request, g

from services import identity
from interfaces.http import validation as v
from interfaces.http.config import Config


class Middleware:
    def __init__(self, config: Config, validator: v.Validator):
        self._config = config
        self._validator = validator

    def _extract(self, request: Any) -> Tuple[str, str, v.Result]:
        header = request.headers.get("Authorization")
        return self._validator.parse_basic_auth_credentials(header)

    def _get_error_response(self, result: v.Result) -> Tuple[Dict, int]:
        return self._validator.find_error_response(result)

    def __call__(self, func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            username, password, result = self._extract(request)
            if not result.success:
                payload, status_code = self._get_error_response(result)
                return payload, status_code
            service = identity.initialize_service(g.database_conn)
            result = service.authenticate_user(username, password)
            if result.success:
                g.subject = username
            return func(*args, **kwargs)

        return _wrapper
