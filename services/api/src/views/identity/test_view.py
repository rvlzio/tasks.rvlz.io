from services.identity import initialize_service
from views.identity import initialize_view
from application import results


def test_user_profile(api_conn):
    service = initialize_service(conn=api_conn)
    sut = initialize_view(conn=api_conn)
    user_id, _ = service.register_user("user", "user@gmail.com", "password")

    profile, result = sut.user_profile(user_id)

    assert result.success
    assert result.error_code is None
    assert len(profile) == 3
    assert profile["id"] == user_id
    assert profile["username"] == "user"
    assert profile["email"] == "user@gmail.com"


def test_missing_user_profile(api_conn):
    sut = initialize_view(conn=api_conn)

    profile, result = sut.user_profile("some_user_id")

    assert not result.success
    assert result.error_code == results.NONEXISTENT_USER_ERR
    assert profile is None


def test_user_profile_by_username(api_conn):
    service = initialize_service(conn=api_conn)
    sut = initialize_view(conn=api_conn)
    user_id, _ = service.register_user("user", "user@gmail.com", "password")

    profile, result = sut.user_profile_by_username("user")

    assert result.success
    assert result.error_code is None
    assert len(profile) == 3
    assert profile["id"] == user_id
    assert profile["username"] == "user"
    assert profile["email"] == "user@gmail.com"


def test_getting_by_username_missing_user_profile(api_conn):
    sut = initialize_view(conn=api_conn)

    profile, result = sut.user_profile_by_username("user")

    assert not result.success
    assert result.error_code == results.NONEXISTENT_USER_ERR
    assert profile is None
