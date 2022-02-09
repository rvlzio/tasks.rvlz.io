import typing

from infrastructure.database import PreparedStatement


prepared_statements = [
    PreparedStatement(
        name="get_user_profile_by_id",
        statement="""
        SELECT username, email FROM api.users WHERE identifier = $1;
        """,
        args=1,
    ),
]


def export() -> typing.List[PreparedStatement]:
    return prepared_statements
