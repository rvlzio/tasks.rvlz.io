import os
import typing

import psycopg2

from config import Config


def generate_connection(config: Config) -> typing.Any:
    user = config.DATABASE_USERNAME
    password = config.DATABASE_PASSWORD
    host = config.DATABASE_HOST
    database = config.DATABASE_NAME
    return psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=5432,
        database=database,
    )
