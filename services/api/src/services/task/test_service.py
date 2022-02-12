import typing

from services.task import initialize_service
from services.task.conftest import (
    GET_TASK_COUNT_BY_ID,
    GET_TASK_BY_ID,
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


def test_task_creation(api_conn, test_conn):
    service = initialize_service(conn=api_conn)

    task_id, result = service.create_task(
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
    service = initialize_service(conn=api_conn, subject_limit=10)

    task_id, result = service.create_task(
        subject="New Phone bill", description="ask for extension"
    )

    assert not result.success
    assert result.error_code == results.TASK_SUBJECT_TOO_LONG
    assert task_id == ""
    assert not task_exists(test_conn, task_id)


def test_task_description_limit(api_conn, test_conn):
    service = initialize_service(conn=api_conn, description_limit=10)

    task_id, result = service.create_task(
        subject="New Phone bill", description="ask for extension"
    )

    assert not result.success
    assert result.error_code == results.TASK_DESCRIPTION_TOO_LONG
    assert task_id == ""
    assert not task_exists(test_conn, task_id)


def test_task_deletion(api_conn, test_conn):
    service = initialize_service(conn=api_conn)
    task_id, result = service.create_task(
        subject="Phone bill", description="ask for extension"
    )

    result = service.delete(task_id)

    assert result.success
    assert result.error_code is None
    assert not task_exists(test_conn, task_id)


def test_deleting_missing_task(api_conn, test_conn):
    service = initialize_service(conn=api_conn)

    result = service.delete("some_task_id")

    assert not result.success
    assert result.error_code == results.NONEXISTENT_TASK_ERR


def test_updating_task(api_conn, test_conn):
    service = initialize_service(conn=api_conn)
    task_id, result = service.create_task(
        subject="Phone bill",
        description="ask for extension",
    )

    result = service.update(
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
    service = initialize_service(conn=api_conn)

    result = service.update(
        "some_task_id",
        subject="Phone bill due",
        description="ask for new extension",
        completed=True,
    )

    assert not result.success
    assert result.error_code == results.NONEXISTENT_TASK_ERR
