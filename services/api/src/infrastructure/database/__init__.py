import os
import typing
from dataclasses import dataclass

import psycopg2


@dataclass
class PreparedStatement:
    name: str
    statement: str
    args: int

    def prepared_statement(self) -> str:
        return f"PREPARE {self.name} AS {self.statement}"

    def execution_statement(self) -> str:
        params = ", ".join(["%s"] * self.args)
        return f"EXECUTE {self.name} ({params})"


def run_prepared_statements(
    conn: typing.Any,
    prepared_statements: typing.List[PreparedStatement],
):
    for ps in prepared_statements:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(ps.prepared_statement())


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
