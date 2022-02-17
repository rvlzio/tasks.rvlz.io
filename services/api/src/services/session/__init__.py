import typing
from datetime import datetime, timedelta

from application import results
from services import Service
from infrastructure.token_store import TokenStore
from infrastructure.token_store.redis import RedisTokenStore
from infrastructure.token_store.hmac import HMACTokenStore
from infrastructure.token_store.hmac.errors import (
    InvalidHMACTag,
    BadBase64Encoding,
    MalformedSessionToken,
)


class SessionService(Service):
    def __init__(self, token_store: TokenStore, duration: int):
        self.token_store = token_store
        self.duration = duration

    def start_session(
        self, username: str
    ) -> typing.Tuple[str, results.Result]:
        expiry = datetime.utcnow() + timedelta(seconds=self.duration)
        token_id = self.token_store.create_token(username, expiry)
        return token_id, results.Result(success=True)

    def end_session(self, token: str) -> results.Result:
        try:
            self.token_store.delete_token(token)
        except InvalidHMACTag:
            return results.Result(
                success=False, error_code=results.INVALID_HMAC_TAG_ERR
            )
        except BadBase64Encoding:
            return results.Result(
                success=False, error_code=results.BAD_BASE64_ENCODING_ERR
            )
        except MalformedSessionToken:
            return results.Result(
                success=False, error_code=results.MALFORMED_SESSION_TOKEN_ERR
            )
        return results.Result(success=True)


def initialize_service(
    conn: typing.Any, secret_key: str, duration: int = 86400
) -> SessionService:
    redis_token_store = RedisTokenStore(conn=conn)
    hmac_token_store = HMACTokenStore(
        key=secret_key, delegate=redis_token_store
    )
    return SessionService(token_store=hmac_token_store, duration=duration)
