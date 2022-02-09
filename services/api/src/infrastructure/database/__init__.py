import os
import typing

import psycopg2


def generate_api_connection(test: bool = False) -> typing.Any:
    user = os.environ.get("DATABASE_USERNAME")
    password = os.environ.get("DATABASE_PASSWORD")
    host = os.environ.get("DATABASE_HOST")
    database = os.environ.get("DATABASE_NAME")
    if test:
        database = os.environ.get("DATABASE_TEST_NAME")
    return psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=5432,
        database=database,
    )


def generate_test_connection():
    user = os.environ.get("DATABASE_TEST_USERNAME")
    password = os.environ.get("DATABASE_TEST_PASSWORD")
    host = os.environ.get("DATABASE_HOST")
    database = os.environ.get("DATABASE_TEST_NAME")
    return psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=5432,
        database=database,
    )
