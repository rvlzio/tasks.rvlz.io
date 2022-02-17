import pytest

from infrastructure import database
from infrastructure.database.prepared_statements import (
    PreparedStatement,
    run_prepared_statements,
)
from infrastructure.database.prepared_statements import sql
from config import initialize_config_factory

config_factory = initialize_config_factory()

USER_COUNT_BY_ID_USERNAME_AND_EMAIL = PreparedStatement(
    name="user_count_by_id_username_and_email",
    statement="""
    SELECT COUNT(*) FROM api.users
    WHERE identifier = $1 AND username = $2 AND email = $3;
    """,
    args=3,
)

USER_COUNT_BY_USERNAME = PreparedStatement(
    name="user_count_by_username",
    statement="""
    SELECT COUNT(*) FROM api.users WHERE username = $1;
    """,
    args=1,
)

USER_COUNT_BY_EMAIL = PreparedStatement(
    name="user_count_by_email",
    statement="""
    SELECT COUNT(*) FROM api.users WHERE email = $1;
    """,
    args=1,
)

test_prepared_statements = [
    USER_COUNT_BY_ID_USERNAME_AND_EMAIL,
    USER_COUNT_BY_USERNAME,
    USER_COUNT_BY_EMAIL,
]


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
            cursor.execute("DELETE FROM api.tasks")
            cursor.execute("DELETE FROM api.users")


@pytest.fixture(scope="function")
def test_conn(raw_test_conn):
    yield raw_test_conn
