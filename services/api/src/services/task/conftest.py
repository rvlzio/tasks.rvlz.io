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

test_prepared_statements = [
    GET_TASK_COUNT_BY_ID,
    GET_TASK_BY_ID,
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


@pytest.fixture(scope="function")
def test_conn(raw_test_conn):
    yield raw_test_conn
