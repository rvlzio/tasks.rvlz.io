import pytest

from services import prepared_statements
from infrastructure import database


USER_COUNT_BY_USERNAME_AND_EMAIL = database.PreparedStatement(
    name="user_count_by_username_and_email",
    statement="""
    SELECT COUNT(*) FROM api.users
    WHERE identifier = $1 AND username = $2 AND email = $3;
    """,
    args=3,
)

test_prepared_statements = [
    USER_COUNT_BY_USERNAME_AND_EMAIL,
]


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
    database.run_prepared_statements(conn, prepared_statements.export())
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
