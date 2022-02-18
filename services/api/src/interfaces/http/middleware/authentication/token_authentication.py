import functools
from typing import Tuple, Dict, Any

from flask import request, g

from interfaces.http import validation as v
from interfaces.http.config import Config
from views import session


class Middleware:
    def __init__(self, config: Config, validator: v.Validator):
        self._config = config
        self._validator = validator

    def _extract(self, request: Any) -> Tuple[str, v.Result]:
        header = request.headers.get("Authorization")
        return self._validator.parse_bearer_auth_credentials(header)

    def _get_error_response(self, result: v.Result) -> Tuple[Dict, int]:
        return self._validator.find_error_response(result)

    def __call__(self, func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            token, result = self._extract(request)
            if not result.success:
                payload, status_code = self._get_error_response(result)
                return payload, status_code
            view = session.initialize_view(
                conn=g.token_store_conn,
                secret_key=self._config.SECRET_KEY,
            )
            username, result = view.session_username(token)
            if result.success:
                g.subject = username
            return func(*args, **kwargs)

        return _wrapper
