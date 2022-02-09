import typing

from infrastructure.token_store.redis import RedisTokenStore
from infrastructure.token_store.hmac import HMACTokenStore
from infrastructure.token_store.hmac.errors import (
    InvalidHMACTag,
)
from infrastructure.token_store import TokenStore
from views import results
from views import View


class SessionView(View):
    def __init__(self, token_store: TokenStore):
        self.token_store = token_store

    def session_username(self, token: str) -> typing.Tuple[str, results.Result]:
        try:
            tk = self.token_store.read_token(token)
        except InvalidHMACTag:
            return "", results.Result(
                success=False, error_code=results.INVALID_HMAC_TAG_ERR
            )
        return tk.username, results.Result(success=True)


def initialize_view(
    conn: typing.Any,
    secret_key: str,
) -> SessionView:
    redis_token_store = RedisTokenStore(conn=conn)
    hmac_token_store = HMACTokenStore(
        key=secret_key, delegate=redis_token_store
    )
    return SessionView(token_store=hmac_token_store)
