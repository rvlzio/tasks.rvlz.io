import typing

from views.task import initialize_view
from services.task import initialize_service

from application import results
from services.task.conftest import (
    CREATE_USER,
)


def create_user(conn: typing.Any) -> str:
    identifier = "id"
    username = "user"
    email = "user@gmail.com"
    password = "password"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                CREATE_USER.execution_statement(),
                (identifier, username, email, password),
            )
    return username


def test_current_task(api_conn, test_conn):
    sut = initialize_view(conn=api_conn)
    service = initialize_service(conn=api_conn)
    task_id, _ = service.create_task(
        subject="Pay phone bill", description="Ask for extension"
    )

    task, result = sut.current_task(task_id)

    assert result.success
    assert result.error_code is None
    assert task == {
        "subject": "Pay phone bill",
        "description": "Ask for extension",
        "completed": False,
    }


def test_missing_current_task(api_conn, test_conn):
    sut = initialize_view(conn=api_conn)

    task, result = sut.current_task("some_task_id")

    assert not result.success
    assert result.error_code == results.NONEXISTENT_TASK_ERR
    assert task is None


def test_current_user_task(api_conn, test_conn):
    username = create_user(test_conn)
    service = initialize_service(conn=api_conn)
    task_id, _ = service.create_user_task(
        username=username,
        subject="Pay phone bill",
        description="Ask for extension",
    )
    sut = initialize_view(conn=api_conn)

    task, result = sut.current_user_task(username, task_id)

    assert result.success
    assert result.error_code is None
    assert task == {
        "subject": "Pay phone bill",
        "description": "Ask for extension",
        "completed": False,
    }


def test_missing_current_user_task(api_conn, test_conn):
    username = create_user(test_conn)
    sut = initialize_view(conn=api_conn)

    task, result = sut.current_user_task(username, "some_task_id")

    assert not result.success
    assert result.error_code == results.NONEXISTENT_TASK_ERR
    assert task is None
