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
        expiry: datetime,
        attributes: typing.Dict[str, str] = {},
    ):
        self.identifier = identifier
        self.username = username
        self.expiry = expiry
        self.attributes = attributes


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


def generate_api_connection(test: bool = False) -> typing.Any:
    username = os.environ.get("TOKEN_STORE_USER")
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
    username = os.environ.get("TOKEN_STORE_TEST_USER")
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
