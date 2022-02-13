import pytest

from infrastructure import database
from infrastructure.database.prepared_statements import (
    PreparedStatement,
    run_prepared_statements,
)
from infrastructure.database.prepared_statements import sql

CREATE_USER = PreparedStatement(
    name="create_user",
    statement="""
    INSERT INTO api.users (identifier, username, email, password_hash)
    VALUES ($1, $2, $3, $4);
    """,
    args=4,
)

test_prepared_statements = [
    CREATE_USER,
]


@pytest.fixture(scope="module")
def raw_test_conn():
    conn = database.generate_test_connection()
    run_prepared_statements(
        conn,
        test_prepared_statements,
    )
    yield conn
    conn.close()


@pytest.fixture(scope="module")
def raw_api_conn():
    conn = database.generate_api_connection(test=True)
    run_prepared_statements(conn, sql.export())
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def api_conn(raw_test_conn, raw_api_conn):
    yield raw_api_conn
    with raw_test_conn:
        with raw_test_conn.cursor() as cursor:
            cursor.execute("DELETE FROM api.tasks")
            cursor.execute("DELETE FROM api.users")


@pytest.fixture(scope="function")
def test_conn(raw_test_conn):
    yield raw_test_conn
