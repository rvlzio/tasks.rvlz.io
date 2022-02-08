import typing
import base64
import hmac
import hashlib
from datetime import datetime

from infrastructure.token_store import TokenStore, Token
from infrastructure.token_store.hmac import errors


class HMACTokenStore(TokenStore):
    def __init__(self, key: str, delegate: TokenStore):
        self.key = key
        self.delegate = delegate

    def _is_valid_hmac_tag(self, message: str, tag: str) -> bool:
        message = base64.b64decode(message.encode("ascii"))
        tag = base64.b64decode(tag.encode("ascii"))
        key = self.key.encode("ascii")
        message_tag = hmac.new(key, message, digestmod=hashlib.sha256).digest()
        return hmac.compare_digest(tag, message_tag)

    def _generate_hmac_tag(self, token_id: str) -> bytes:
        key = self.key.encode("ascii")
        message = base64.b64decode(token_id.encode("ascii"))
        return hmac.new(key, message, digestmod=hashlib.sha256).digest()

    def create_token(
        self,
        username: str,
        expiry: datetime,
        attributes: typing.Dict[str, str] = {},
    ) -> str:
        token_id = self.delegate.create_token(username, expiry, attributes)
        tag = self._generate_hmac_tag(token_id)
        tag = base64.b64encode(tag).decode("ascii")
        return f"{token_id}.{tag}"

    def delete_token(self, token_id: str):
        token_id, tag = token_id.split(".")
        if not self._is_valid_hmac_tag(token_id, tag):
            raise errors.InvalidHMACTag()
        self.delegate.delete_token(token_id)
