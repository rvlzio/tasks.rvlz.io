import typing
import base64
import hashlib
import hmac

import pytest

from services.session import initialize_service
from services import results


def hmac_tag_valid(secret_key: str, token: str) -> bool:
    token_id, tag = token.split(".")
    # decode token_id, tag, key to bytes
    token_id = base64.b64decode(token_id.encode("ascii"))
    tag = base64.b64decode(tag.encode("ascii"))
    key = secret_key.encode("ascii")
    # generate token_id tag
    token_id_tag = hmac.new(key, token_id, digestmod=hashlib.sha256).digest()
    # compare tags
    return hmac.compare_digest(tag, token_id_tag)


def session_in_store(conn: typing.Any, token: str) -> bool:
    token_id = token.split(".")[0]
    # decode to bytes
    token_id = base64.b64decode(token_id.encode("ascii"))
    m = hashlib.sha256()
    m.update(token_id)
    hashed_token_id = base64.b64encode(m.digest()).decode("ascii")
    count = conn.exists(f"tk_id:{hashed_token_id}")
    return count == 1


def session_removed_from_store(conn: typing.Any, token: str) -> bool:
    token_id = token.split(".")[0]
    token_id = base64.b64decode(token_id.encode("ascii"))
    m = hashlib.sha256()
    m.update(token_id)
    hashed_token_id = base64.b64encode(m.digest()).decode("ascii")
    count = conn.exists(f"tk_id:{hashed_token_id}")
    return count == 0


def username_in_stored_session(
    conn: typing.Any,
    token: str,
    username: str,
) -> bool:
    token_id = token.split(".")[0]
    # decode to bytes
    token_id = base64.b64decode(token_id.encode("ascii"))
    m = hashlib.sha256()
    m.update(token_id)
    hashed_token_id = base64.b64encode(m.digest()).decode("ascii")
    data = conn.hmget(f"tk_id:{hashed_token_id}", keys=["username"])
    session_username = data[0]
    return username == session_username


def test_session_start(api_conn, test_conn):
    secret_key = "my_secret"
    service = initialize_service(conn=api_conn, secret_key=secret_key)

    token, result = service.start_session("user")

    assert result.success
    assert result.error_code is None
    assert hmac_tag_valid(secret_key, token)
    assert session_in_store(test_conn, token)
    assert username_in_stored_session(test_conn, token, "user")


def test_session_end(api_conn, test_conn):
    secret_key = "my_secret"
    service = initialize_service(conn=api_conn, secret_key=secret_key)
    token, _ = service.start_session("user")

    result = service.end_session(token)

    assert result.success
    assert result.error_code is None
    assert session_removed_from_store(test_conn, token)


def test_invalid_hmac_tag_cannot_end_session(api_conn, test_conn):
    secret_key = "my_secret"
    service = initialize_service(conn=api_conn, secret_key=secret_key)
    token, _ = service.start_session("user")
    malformed_token = token.split(".")[0] + "." + "invalid_hmac_tag=="

    result = service.end_session(malformed_token)

    assert not result.success
    assert result.error_code == results.INVALID_HMAC_TAG_ERR
    assert session_in_store(test_conn, token)


@pytest.mark.parametrize(
    "bad_token",
    [
        "你好世界.hmac_tag==",
        "token_identifier==.你好世界",
        "你好世界.你好世界",
    ],
)
def test_invalid_base64_tag_cannot_end_session(api_conn, test_conn, bad_token):
    secret_key = "my_secret"
    service = initialize_service(conn=api_conn, secret_key=secret_key)

    result = service.end_session(bad_token)

    assert not result.success
    assert result.error_code == results.BAD_BASE64_ENCODING_ERR


@pytest.mark.parametrize(
    "bad_token",
    [
        "token_identifier==hmac_tag==",
        "token_identifier==.",
        ".hmac_tag==",
    ],
)
def test_malformed_token_cannot_end_session(api_conn, test_conn, bad_token):
    secret_key = "my_secret"
    service = initialize_service(conn=api_conn, secret_key=secret_key)

    result = service.end_session(bad_token)

    assert not result.success
    assert result.error_code == results.MALFORMED_SESSION_TOKEN_ERR
