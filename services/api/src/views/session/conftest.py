import pytest

from infrastructure import token_store
from config import initialize_config_factory

config_factory = initialize_config_factory()


@pytest.fixture(scope="module")
def raw_test_conn():
    config = config_factory.load(privileged=True)
    conn = token_store.generate_connection(config)
    yield conn


@pytest.fixture(scope="function")
def test_conn(raw_test_conn):
    yield raw_test_conn
    raw_test_conn.flushall()


@pytest.fixture(scope="module")
def api_conn():
    config = config_factory.load(test=True)
    conn = token_store.generate_connection(config)
    yield conn
