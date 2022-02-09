import typing

from psycopg2.errors import UniqueViolation

from services.identity.security import HashingAlgorithm
from services.identity.security.scrypt import Scrypt
from services import Service
from application import results
from infrastructure.database.prepared_statements import sql


class IdentityService(Service):
    def __init__(
        self,
        conn: typing.Any,
        hashing_algorithm: HashingAlgorithm = Scrypt(),
    ):
        self.conn = conn
        self.hashing_algorithm = hashing_algorithm
        self.prepared_statements = sql.export()

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
    ) -> typing.Tuple[str, results.Result]:
        try:
            identifier = self.generate_unique_id()
            password_hash = self.hashing_algorithm.run(password)
            with self.conn:
                with self.conn.cursor() as cursor:
                    prepared_statement = self.find_prepared_statement(
                        "add_user"
                    )
                    cursor.execute(
                        prepared_statement.execution_statement(),
                        (identifier, username, email, password_hash),
                    )
            return identifier, results.Result(success=True)
        except UniqueViolation as exc:
            error_code = None
            exc_message = str(exc)
            if '"users_username_key"' in exc_message:
                error_code = results.DUPLICATE_USERNAME_ERR
            elif '"users_email_key"' in exc_message:
                error_code = results.DUPLICATE_EMAIL_ERR
            return "", results.Result(success=False, error_code=error_code)

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> results.Result:
        with self.conn:
            with self.conn.cursor() as cursor:
                prepared_statement = self.find_prepared_statement(
                    "get_password_hash_by_username"
                )
                cursor.execute(
                    prepared_statement.execution_statement(),
                    (username,),
                )
                row = cursor.fetchone()
                if row is None:
                    return results.Result(
                        success=False, error_code=results.NONEXISTENT_USER_ERR
                    )
                password_hash = row[0]
                is_authenticated = self.hashing_algorithm.verify(
                    password,
                    password_hash,
                )
                if is_authenticated:
                    return results.Result(success=True)
                return results.Result(
                    success=False, error_code=results.INVALID_CREDENTIALS_ERR
                )
        return results.Result(success=True)


def initialize_service(conn: typing.Any) -> IdentityService:
    return IdentityService(conn=conn)
