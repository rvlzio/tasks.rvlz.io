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
]


def export() -> typing.List[PreparedStatement]:
    return prepared_statements
