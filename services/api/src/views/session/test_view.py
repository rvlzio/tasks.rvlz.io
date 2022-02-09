from services.session import initialize_service
from views.session import initialize_view


def test_session_username(api_conn, test_conn):
    secret_key = "secret_key"
    service = initialize_service(conn=test_conn, secret_key=secret_key)
    token, _ = service.start_session("user")
    view = initialize_view(conn=api_conn, secret_key=secret_key)

    username, result = view.session_username(token)

    assert result.success
    assert result.error_code is None
    assert username == "user"
