import pytest

from infrastructure import database
from infrastructure.database.prepared_statements import (
    PreparedStatement,
    run_prepared_statements,
)
from infrastructure.database.prepared_statements import sql

GET_TASK_COUNT_BY_ID = PreparedStatement(
    name="get_task_count_by_id",
    statement="""
    SELECT COUNT(*) FROM api.tasks WHERE identifier = $1;
    """,
    args=1,
)

GET_TASK_BY_ID = PreparedStatement(
    name="get_task_by_id",
    statement="""
    SELECT subject, description, completed FROM api.tasks
    WHERE identifier = $1;
    """,
    args=1,
)

CREATE_USER = PreparedStatement(
    name="create_user",
    statement="""
    INSERT INTO api.users (identifier, username, email, password_hash)
    VALUES ($1, $2, $3, $4);
    """,
    args=4,
)

GET_USER_TASK_COUNT_BY_ID = PreparedStatement(
    name="get_user_task_count_by_id",
    statement="""
    SELECT COUNT(*) FROM api.users INNER JOIN api.tasks
    ON api.users._pk = api.tasks._user_pk
    WHERE api.tasks.identifier = $1 AND api.users.username = $2;
    """,
    args=2,
)

test_prepared_statements = [
    GET_TASK_COUNT_BY_ID,
    GET_TASK_BY_ID,
    CREATE_USER,
    GET_USER_TASK_COUNT_BY_ID,
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
