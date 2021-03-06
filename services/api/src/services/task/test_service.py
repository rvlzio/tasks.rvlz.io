import typing

from services.task import initialize_service
from services.task.conftest import (
    GET_TASK_COUNT_BY_ID,
    GET_TASK_BY_ID,
    CREATE_USER,
    GET_USER_TASK_COUNT_BY_ID,
)
from application import results


def task_exists(conn: typing.Any, task_id: str) -> bool:
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                GET_TASK_COUNT_BY_ID.execution_statement(),
                (task_id,),
            )
            row = cursor.fetchone()
            count = row[0]
            return count == 1


def task_field_values(
    conn: typing.Any,
    task_id: str,
    subject: str,
    description: str,
    completed: bool,
) -> bool:
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                GET_TASK_BY_ID.execution_statement(),
                (task_id,),
            )
            row = cursor.fetchone()
            return (
                subject == row[0]
                and description == row[1]
                and completed == row[2]
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


def one_user_task_exists(
    conn: typing.Any, username: str, task_id: str
) -> bool:
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                GET_USER_TASK_COUNT_BY_ID.execution_statement(),
                (task_id, username),
            )
            row = cursor.fetchone()
            count = row[0]
    return count == 1


def test_task_creation(api_conn, test_conn):
    sut = initialize_service(conn=api_conn)

    task_id, result = sut.create_task(
        subject="Phone bill", description="ask for extension"
    )

    assert result.success is True
    assert result.error_code is None
    assert task_id != ""
    assert task_exists(test_conn, task_id)
    assert task_field_values(
        conn=test_conn,
        task_id=task_id,
        subject="Phone bill",
        description="ask for extension",
        completed=False,
    )


def test_task_subject_limit(api_conn, test_conn):
    sut = initialize_service(conn=api_conn, subject_limit=10)

    task_id, result = sut.create_task(
        subject="New Phone bill", description="ask for extension"
    )

    assert not result.success
    assert result.error_code == results.TASK_SUBJECT_TOO_LONG
    assert task_id == ""
    assert not task_exists(test_conn, task_id)


def test_task_description_limit(api_conn, test_conn):
    sut = initialize_service(conn=api_conn, description_limit=10)

    task_id, result = sut.create_task(
        subject="New Phone bill", description="ask for extension"
    )

    assert not result.success
    assert result.error_code == results.TASK_DESCRIPTION_TOO_LONG
    assert task_id == ""
    assert not task_exists(test_conn, task_id)


def test_task_deletion(api_conn, test_conn):
    sut = initialize_service(conn=api_conn)
    task_id, result = sut.create_task(
        subject="Phone bill", description="ask for extension"
    )

    result = sut.delete_task(task_id)

    assert result.success
    assert result.error_code is None
    assert not task_exists(test_conn, task_id)


def test_deleting_missing_task(api_conn, test_conn):
    sut = initialize_service(conn=api_conn)

    result = sut.delete_task("some_task_id")

    assert not result.success
    assert result.error_code == results.NONEXISTENT_TASK_ERR


def test_updating_task(api_conn, test_conn):
    sut = initialize_service(conn=api_conn)
    task_id, result = sut.create_task(
        subject="Phone bill",
        description="ask for extension",
    )

    result = sut.update_task(
        task_id,
        subject="Phone bill due",
        description="ask for new extension",
        completed=True,
    )

    assert result.success
    assert result.error_code is None
    assert task_field_values(
        conn=test_conn,
        task_id=task_id,
        subject="Phone bill due",
        description="ask for new extension",
        completed=True,
    )


def test_updating_missing_task(api_conn, test_conn):
    sut = initialize_service(conn=api_conn)

    result = sut.update_task(
        "some_task_id",
        subject="Phone bill due",
        description="ask for new extension",
        completed=True,
    )

    assert not result.success
    assert result.error_code == results.NONEXISTENT_TASK_ERR


def test_creating_user_task(api_conn, test_conn):
    username = create_user(test_conn)
    sut = initialize_service(conn=api_conn)

    task_id, result = sut.create_user_task(
        username=username,
        subject="Phone bill",
        description="ask for extension",
    )

    assert result.success
    assert result.error_code is None
    assert one_user_task_exists(test_conn, username, task_id)


def test_user_task_subject_limit(api_conn, test_conn):
    username = create_user(test_conn)
    sut = initialize_service(conn=api_conn, subject_limit=10)

    task_id, result = sut.create_user_task(
        username=username,
        subject="New Phone bill",
        description="ask for extension",
    )

    assert not result.success
    assert result.error_code == results.TASK_SUBJECT_TOO_LONG
    assert task_id == ""
    assert not one_user_task_exists(test_conn, username, task_id)


def test_user_task_description_limit(api_conn, test_conn):
    username = create_user(test_conn)
    sut = initialize_service(conn=api_conn, description_limit=10)

    task_id, result = sut.create_user_task(
        username=username,
        subject="New Phone bill",
        description="ask for extension",
    )

    assert not result.success
    assert result.error_code == results.TASK_DESCRIPTION_TOO_LONG
    assert task_id == ""
    assert not one_user_task_exists(test_conn, username, task_id)


def test_delete_user_task(api_conn, test_conn):
    username = create_user(test_conn)
    sut = initialize_service(conn=api_conn)
    task_id, _ = sut.create_user_task(
        username=username,
        subject="Phone bill",
        description="ask for extension",
    )

    result = sut.delete_user_task(username=username, task_id=task_id)

    assert result.success
    assert result.error_code is None
    assert not one_user_task_exists(test_conn, username, task_id)


def test_deleting_missing_user_task(api_conn, test_conn):
    username = create_user(test_conn)
    sut = initialize_service(conn=api_conn)

    result = sut.delete_user_task(username=username, task_id="some_task_id")

    assert not result.success
    assert result.error_code == results.NONEXISTENT_TASK_ERR


def test_updating_user_task(api_conn, test_conn):
    username = create_user(test_conn)
    sut = initialize_service(conn=api_conn)
    task_id, _ = sut.create_user_task(
        username=username,
        subject="Phone bill",
        description="ask for extension",
    )

    result = sut.update_user_task(
        username=username,
        task_id=task_id,
        subject="Phone bill due",
        description="ask for new extension",
        completed=True,
    )

    assert result.success
    assert result.error_code is None
    assert task_field_values(
        conn=test_conn,
        task_id=task_id,
        subject="Phone bill due",
        description="ask for new extension",
        completed=True,
    )


def test_updating_missing_user_task(api_conn, test_conn):
    username = create_user(test_conn)
    sut = initialize_service(conn=api_conn)

    result = sut.update_user_task(
        username=username,
        task_id="some_task_id",
        subject="Phone bill due",
        description="ask for new extension",
        completed=True,
    )

    assert not result.success
    assert result.error_code == results.NONEXISTENT_TASK_ERR
