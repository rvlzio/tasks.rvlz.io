import typing

from services.identity import IdentityService
from services.identity.conftest import (
    USER_COUNT_BY_ID_USERNAME_AND_EMAIL,
    USER_COUNT_BY_USERNAME,
)
from services import results


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


def user_count_by_username(conn: typing.Any, username: str) -> int:
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                USER_COUNT_BY_USERNAME.execution_statement(),
                (username,),
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


def test_user_registration_with_taken_username(api_conn, test_conn):
    service = IdentityService(conn=api_conn)
    username, email, password = "user", "user@gmail.com", "password"
    service.register_user(username, email, password)
    other_email, other_password = "other_user@gmail.com", "other_password"

    identifier, result = service.register_user(
        "user",
        other_email,
        other_password,
    )

    assert not result.success
    assert result.error_code == results.DUPLICATE_USERNAME_ERR
    assert user_count_by_username(test_conn, "user") == 1
