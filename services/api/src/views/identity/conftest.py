import pytest

from infrastructure import database
from infrastructure.database.prepared_statements import (
    PreparedStatement,
    run_prepared_statements,
)
from infrastructure.database.prepared_statements import sql


test_prepared_statements = []


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
            cursor.execute("DELETE FROM api.users")


@pytest.fixture(scope="function")
def test_conn(raw_test_conn):
    yield raw_test_conn