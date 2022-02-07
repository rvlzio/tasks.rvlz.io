import typing

from services.identity import IdentityService
from services.identity.conftest import (
    USER_COUNT_BY_ID_USERNAME_AND_EMAIL,
)


def user_count(
    conn: typing.Any,
    identifier: str,
    username: str,
    email: str,
) -> int:
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                USER_COUNT_BY_ID_USERNAME_AND_EMAIL.execution_statement(),
                (identifier, username, email),
            )
            row = cursor.fetchone()
            return row[0]


def test_user_registration(api_conn, test_conn):
    service = IdentityService(conn=api_conn)
    username, email, password = "user", "user@gmail.com", "password"

    identifier, result = service.register_user(username, email, password)

    assert result.success
    assert result.error_code is None
    assert user_count(test_conn, identifier, username, email) == 1
