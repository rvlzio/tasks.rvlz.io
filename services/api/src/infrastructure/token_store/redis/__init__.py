import os
import typing
import base64
import hashlib
import json
from datetime import datetime

from infrastructure import token_store


class RedisTokenStore(token_store.TokenStore):
    def __init__(self, conn: typing.Any):
        self.conn = conn

    def _generate_random_token_id(self) -> str:
        return base64.b64encode(os.urandom(20)).decode("ascii")

    def _hash(self, token_id: str) -> str:
        token_id = base64.b64decode(token_id.encode("ascii"))
        m = hashlib.sha256()
        m.update(token_id)
        return base64.b64encode(m.digest()).decode("ascii")

    def create_token(
        self,
        username: str,
        expiry: datetime,
        attributes: typing.Dict[str, str] = {},
    ) -> str:
        token_id = self._generate_random_token_id()
        hashed_token_id = self._hash(token_id)
        mapping = {
            "username": username,
            "expiry": expiry.strftime("%Y-%m-%d %H:%M:%S"),
            "attributes": json.dumps(attributes, separators=[",", ":"]),
        }
        self.conn.hset(f"tk_id:{hashed_token_id}", mapping=mapping)
        return token_id

    def delete_token(self, token_id: str):
        hashed_token_id = self._hash(token_id)
        key = f"tk_id:{hashed_token_id}"
        self.conn.delete(key)
