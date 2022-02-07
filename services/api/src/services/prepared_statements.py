import typing

from infrastructure.database import PreparedStatement


prepared_statements = [
    PreparedStatement(
        name="add_user",
        statement="""
        INSERT INTO api.users (identifier, username, email, password_hash)
        VALUES ($1, $2, $3, $4);
        """,
        args=4,
    ),
    PreparedStatement(
        name="get_password_hash_by_username",
        statement="""
        SELECT password_hash FROM api.users WHERE username = $1 LIMIT 1;
        """,
        args=1,
    ),
]


def export() -> typing.List[PreparedStatement]:
    return prepared_statements
