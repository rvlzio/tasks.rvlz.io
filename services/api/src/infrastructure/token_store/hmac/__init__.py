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

    def _has_valid_form(self, token_id: str) -> bool:
        components = token_id.split(".")
        return (
            len(components) == 2
            and components[0] != ""
            and components[1] != ""
        )

    def _is_valid_base64(self, s: str) -> bool:
        try:
            base64.b64decode(s.encode("ascii"))
            return True
        except Exception:
            return False

    def _is_valid_hmac_tag(self, message: str, tag: str) -> bool:
        message = base64.b64decode(message.encode("ascii"))
        tag = base64.b64decode(tag.encode("ascii"))
        key = self.key.encode("ascii")
        message_tag = hmac.new(key, message, digestmod=hashlib.sha256).digest()
        return hmac.compare_digest(tag, message_tag)

    def _extract_token_id(self, token: str) -> str:
        if not self._has_valid_form(token):
            raise errors.MalformedSessionToken()
        token_id, tag = token.split(".")
        if not self._is_valid_base64(token_id) or not self._is_valid_base64(
            tag
        ):
            raise errors.BadBase64Encoding()
        if not self._is_valid_hmac_tag(token_id, tag):
            raise errors.InvalidHMACTag()
        return token_id

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

    def read_token(self, token_id: str) -> typing.Optional[Token]:
        unsigned_token_id = self._extract_token_id(token_id)
        token = self.delegate.read_token(unsigned_token_id)
        return token

    def delete_token(self, token_id: str):
        unsigned_token_id = self._extract_token_id(token_id)
        self.delegate.delete_token(unsigned_token_id)
