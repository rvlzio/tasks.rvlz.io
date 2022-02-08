import typing
import base64
import hashlib
import hmac

from services.session import initialize_service


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
