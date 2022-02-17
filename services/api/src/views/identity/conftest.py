import pytest

from infrastructure import database
from infrastructure.database.prepared_statements import (
    PreparedStatement,
    run_prepared_statements,
)
from infrastructure.database.prepared_statements import sql
from config import initialize_config_factory

config_factory = initialize_config_factory()

test_prepared_statements = []


@pytest.fixture(scope="module")
def raw_test_conn():
    config = config_factory.load(privileged=True)
    conn = database.generate_connection(config)
    run_prepared_statements(
        conn,
        test_prepared_statements,
    )
    yield conn
    conn.close()


@pytest.fixture(scope="module")
def raw_api_conn():
    config = config_factory.load(test=True)
    conn = database.generate_connection(config)
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
