import pytest

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


@pytest.mark.parametrize(
    "bad_token",
    [
        "你好世界.hmac_tag==",
        "token_identifier==.你好世界",
        "你好世界.你好世界",
    ],
)
def test_session_username_with_bad_base64_tag(api_conn, test_conn, bad_token):
    secret_key = "my_secret"
    service = initialize_service(conn=test_conn, secret_key=secret_key)
    token, _ = service.start_session("user")
    view = initialize_view(conn=api_conn, secret_key=secret_key)

    username, result = view.session_username(bad_token)

    assert not result.success
    assert result.error_code == results.BAD_BASE64_ENCODING_ERR
    assert username == ""


@pytest.mark.parametrize(
    "bad_token",
    [
        "token_identifier==hmac_tag==",
        "token_identifier==.",
        ".hmac_tag==",
    ],
)
def test_session_username_with_malformed_tag(api_conn, test_conn, bad_token):
    secret_key = "my_secret"
    service = initialize_service(conn=test_conn, secret_key=secret_key)
    token, _ = service.start_session("user")
    view = initialize_view(conn=api_conn, secret_key=secret_key)

    username, result = view.session_username(bad_token)

    assert not result.success
    assert result.error_code == results.MALFORMED_SESSION_TOKEN_ERR
    assert username == ""


def test_username_of_nonexisting_session(api_conn, test_conn):
    secret_key = "secret_key"
    service = initialize_service(conn=test_conn, secret_key=secret_key)
    token, _ = service.start_session("user")
    service.end_session(token)
    view = initialize_view(conn=api_conn, secret_key=secret_key)

    username, result = view.session_username(token)

    assert not result.success
    assert result.error_code == results.MISSING_SESSION_ERR
    assert username == ""
