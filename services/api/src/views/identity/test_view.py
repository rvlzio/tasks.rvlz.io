from services.identity import initialize_service
from views.identity import initialize_view


def test_user_profile(api_conn):
    service = initialize_service(conn=api_conn)
    view = initialize_view(conn=api_conn)
    user_id, _ = service.register_user("user", "user@gmail.com", "password")

    profile, result = view.user_profile(user_id)

    assert result.success
    assert result.error_code is None
    assert len(profile) == 2
    assert profile["username"] == "user"
    assert profile["email"] == "user@gmail.com"
