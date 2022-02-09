from services.session import initialize_service
from views.session import initialize_view
from views import results


def test_session_username(api_conn, test_conn):
    secret_key = "secret_key"
    service = initialize_service(conn=test_conn, secret_key=secret_key)
    token, _ = service.start_session("user")
    view = initialize_view(conn=api_conn, secret_key=secret_key)

    username, result = view.session_username(token)

    assert result.success
    assert result.error_code is None
    assert username == "user"


def test_session_username_with_invalid_hmac_tag(api_conn, test_conn):
    secret_key = "my_secret"
    service = initialize_service(conn=test_conn, secret_key=secret_key)
    token, _ = service.start_session("user")
    malformed_token = token.split(".")[0] + "." + "invalid_hmac_tag=="
    view = initialize_view(conn=api_conn, secret_key=secret_key)

    username, result = view.session_username(malformed_token)

    assert not result.success
    assert result.error_code == results.INVALID_HMAC_TAG_ERR
    assert username == ""
