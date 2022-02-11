import typing

from infrastructure.database.prepared_statements import PreparedStatement


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
    PreparedStatement(
        name="get_user_profile_by_id",
        statement="""
        SELECT username, email FROM api.users WHERE identifier = $1;
        """,
        args=1,
    ),
    PreparedStatement(
        name="add_task",
        statement="""
        INSERT INTO api.tasks (identifier, subject, description, completed)
        VALUES ($1, $2, $3, FALSE);
        """,
        args=3,
    ),
    PreparedStatement(
        name="remove_task",
        statement="""
        WITH deleted AS
        (DELETE FROM api.tasks WHERE identifier = $1 RETURNING *)
        SELECT COUNT(*) FROM deleted;
        """,
        args=1,
    ),
    PreparedStatement(
        name="change_task_subject",
        statement="""
        UPDATE api.tasks SET subject = $1 WHERE identifier = $2;
        """,
        args=2,
    ),
]


def export() -> typing.List[PreparedStatement]:
    return prepared_statements
