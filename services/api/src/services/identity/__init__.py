import typing

from psycopg2.errors import UniqueViolation

from services.identity.security import HashingAlgorithm
from services.identity.security.scrypt import Scrypt
from services import Service
from services import results
from services import prepared_statements


class IdentityService(Service):
    def __init__(
        self,
        conn: typing.Any,
        hashing_algorithm: HashingAlgorithm = Scrypt(),
    ):
        self.conn = conn
        self.hashing_algorithm = hashing_algorithm
        self.prepared_statements = prepared_statements.export()

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
        except UniqueViolation:
            return "", results.Result(
                success=False, error_code=results.DUPLICATE_USERNAME_ERR
            )
