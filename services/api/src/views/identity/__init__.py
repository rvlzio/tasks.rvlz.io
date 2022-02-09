from typing import Optional, Dict, Tuple, Any

from views import View
from application import results
from infrastructure.database.prepared_statements import sql


class IdentityView(View):
    def __init__(self, conn: Any):
        self.conn = conn
        self.prepared_statements = sql.export()

    def user_profile(
        self,
        user_id: str,
    ) -> Tuple[Optional[Dict[str, str]], results.Result]:
        with self.conn:
            with self.conn.cursor() as cursor:
                prepared_statement = self.find_prepared_statement(
                    "get_user_profile_by_id"
                )
                cursor.execute(
                    prepared_statement.execution_statement(), (user_id,)
                )
                row = cursor.fetchone()
                username, email = row
                profile = {
                    "username": username,
                    "email": email,
                }
        return profile, results.Result(success=True)


def initialize_view(conn: Any) -> IdentityView:
    return IdentityView(conn=conn)
