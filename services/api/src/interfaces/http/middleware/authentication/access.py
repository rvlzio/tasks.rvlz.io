import functools

from flask import g


class Middleware:
    def __call__(self, func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            if "subject" not in g:
                return {
                    "code": "authentication_failure",
                    "message": "Authentication required to access endpoint.",
                }, 401
            return func(*args, **kwargs)

        return _wrapper
