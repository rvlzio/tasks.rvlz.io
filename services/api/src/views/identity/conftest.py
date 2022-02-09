import pytest

from services import prepared_statements as services_ps
from views import prepared_statements as views_ps
from infrastructure import database

test_prepared_statements = []


@pytest.fixture(scope="module")
def raw_test_conn():
    conn = database.generate_test_connection()
    database.run_prepared_statements(
        conn,
        test_prepared_statements,
    )
    yield conn
    conn.close()


@pytest.fixture(scope="module")
def raw_api_conn():
    conn = database.generate_api_connection(test=True)
    database.run_prepared_statements(
        conn, services_ps.export() + views_ps.export()
    )
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
