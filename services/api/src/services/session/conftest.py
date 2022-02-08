import pytest

from infrastructure import token_store


@pytest.fixture(scope="module")
def raw_test_conn():
    conn = token_store.generate_test_connection()
    yield conn


@pytest.fixture(scope="function")
def test_conn(raw_test_conn):
    yield raw_test_conn
    raw_test_conn.flushall()


@pytest.fixture(scope="module")
def api_conn():
    conn = token_store.generate_api_connection(test=True)
    yield conn
