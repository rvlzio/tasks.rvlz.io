from views.task import initialize_view
from services.task import initialize_service


def test_current_task(api_conn, test_conn):
    view = initialize_view(conn=api_conn)
    service = initialize_service(conn=api_conn)
    task_id, _ = service.create(
        subject="Pay phone bill", description="Ask for extension"
    )

    task, result = view.current(task_id)

    assert result.success
    assert result.error_code is None
    assert task == {
        "subject": "Pay phone bill",
        "description": "Ask for extension",
        "completed": False,
    }
