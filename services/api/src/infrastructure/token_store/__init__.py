import os
import typing
from abc import ABC, abstractmethod
from datetime import datetime

import redis as rd


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


def generate_api_connection(test: bool = False) -> typing.Any:
    username = os.environ.get("TOKEN_STORE_USERNAME")
    password = os.environ.get("TOKEN_STORE_PASSWORD")
    host = os.environ.get("TOKEN_STORE_HOST")
    db = os.environ.get("TOKEN_STORE_NAME")
    if test:
        db = os.environ.get("TOKEN_STORE_TEST_NAME")
    conn = rd.Redis(
        username=username,
        password=password,
        host=host,
        db=db,
        decode_responses=True,
    )
    conn.ping()
    return conn


def generate_test_connection() -> typing.Any:
    username = os.environ.get("TOKEN_STORE_TEST_USERNAME")
    password = os.environ.get("TOKEN_STORE_TEST_PASSWORD")
    host = os.environ.get("TOKEN_STORE_HOST")
    db = os.environ.get("TOKEN_STORE_TEST_NAME")
    conn = rd.Redis(
        username=username,
        password=password,
        host=host,
        db=db,
        decode_responses=True,
    )
    conn.ping()
    return conn
