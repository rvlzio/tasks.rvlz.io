import os
import typing
from abc import ABC, abstractmethod
from datetime import datetime

import redis as rd

from config import Config


class Token:
    def __init__(
        self,
        identifier: str,
        username: str,
    ):
        self.identifier = identifier
        self.username = username


class TokenStore(ABC):
    @abstractmethod
    def create_token(
        self,
        username: str,
        expiry: datetime,
        attributes: typing.Dict[str, str] = {},
    ) -> str:
        pass

    @abstractmethod
    def delete_token(self, token_id: str):
        pass

    @abstractmethod
    def read_token(self, token_id: str) -> typing.Optional[Token]:
        pass


def generate_connection(config: Config) -> typing.Any:
    username = config.TOKEN_STORE_USERNAME
    password = config.TOKEN_STORE_PASSWORD
    host = config.TOKEN_STORE_HOST
    db = config.TOKEN_STORE_NAME
    conn = rd.Redis(
        username=username,
        password=password,
        host=host,
        db=db,
        decode_responses=True,
    )
    conn.ping()
    return conn
