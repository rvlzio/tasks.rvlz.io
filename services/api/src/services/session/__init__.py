import typing
from datetime import datetime, timedelta

from services import results
from services import Service
from infrastructure.token_store import TokenStore
from infrastructure.token_store.redis import RedisTokenStore
from infrastructure.token_store.hmac import HMACTokenStore


class SessionService(Service):
    def __init__(self, token_store: TokenStore, duration: int):
        self.token_store = token_store
        self.duration = duration

    def start_session(self, username: str) -> typing.Tuple[str, results.Result]:
        expiry = datetime.utcnow() + timedelta(seconds=self.duration)
        token_id = self.token_store.create_token(username, expiry)
        return token_id, results.Result(success=True)

    def end_session(self, token: str) -> results.Result:
        self.token_store.delete_token(token)
        return results.Result(success=True)


def initialize_service(
    conn: typing.Any, secret_key: str, duration: int = 86400
) -> SessionService:
    redis_token_store = RedisTokenStore(conn=conn)
    hmac_token_store = HMACTokenStore(
        key=secret_key, delegate=redis_token_store
    )
    return SessionService(token_store=hmac_token_store, duration=duration)
