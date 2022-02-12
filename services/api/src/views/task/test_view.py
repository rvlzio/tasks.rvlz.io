from views.task import initialize_view
from services.task import initialize_service

from application import results


def test_current_task(api_conn, test_conn):
    sut = initialize_view(conn=api_conn)
    service = initialize_service(conn=api_conn)
    task_id, _ = service.create_task(
        subject="Pay phone bill", description="Ask for extension"
    )

    task, result = sut.current(task_id)

    assert result.success
    assert result.error_code is None
    assert task == {
        "subject": "Pay phone bill",
        "description": "Ask for extension",
        "completed": False,
    }


def test_missing_current_task(api_conn, test_conn):
    sut = initialize_view(conn=api_conn)

    task, result = sut.current("some_task_id")

    assert not result.success
    assert result.error_code == results.NONEXISTENT_TASK_ERR
    assert task is None
