import typing

from infrastructure.token_store.redis import RedisTokenStore
from infrastructure.token_store.hmac import HMACTokenStore
from infrastructure.token_store.hmac.errors import (
    InvalidHMACTag,
    BadBase64Encoding,
    MalformedSessionToken,
)
from infrastructure.token_store import TokenStore
from application import results
from views import View


class SessionView(View):
    def __init__(self, token_store: TokenStore):
        self.token_store = token_store

    def session_username(self, token: str) -> typing.Tuple[str, results.Result]:
        try:
            token = self.token_store.read_token(token)
            if token is None:
                return "", results.Result(
                    success=False, error_code=results.MISSING_SESSION_ERR
                )
            return token.username, results.Result(success=True)
        except InvalidHMACTag:
            return "", results.Result(
                success=False, error_code=results.INVALID_HMAC_TAG_ERR
            )
        except BadBase64Encoding:
            return "", results.Result(
                success=False, error_code=results.BAD_BASE64_ENCODING_ERR
            )
        except MalformedSessionToken:
            return "", results.Result(
                success=False, error_code=results.MALFORMED_SESSION_TOKEN_ERR
            )


def initialize_view(
    conn: typing.Any,
    secret_key: str,
) -> SessionView:
    redis_token_store = RedisTokenStore(conn=conn)
    hmac_token_store = HMACTokenStore(
        key=secret_key, delegate=redis_token_store
    )
    return SessionView(token_store=hmac_token_store)
