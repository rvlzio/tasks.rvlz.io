import os
import typing

import psycopg2

from config import Config
from infrastructure.database.prepared_statements import run_prepared_statements
from infrastructure.database.prepared_statements import sql


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


def run_all_prepared_statements(conn: typing.Any):
    run_prepared_statements(conn, sql.export())
