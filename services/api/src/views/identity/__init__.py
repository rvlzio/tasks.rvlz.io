from typing import Optional, Dict, Tuple, Any

from views import View
from application import results


class IdentityView(View):
    def __init__(self, conn: Any):
        self.conn = conn
        super().__init__()

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
                if row is None:
                    return None, results.Result(
                        success=False,
                        error_code=results.NONEXISTENT_USER_ERR,
                    )
                username, email = row
                profile = {
                    "username": username,
                    "email": email,
                }
        return profile, results.Result(success=True)

    def user_profile_by_username(
        self,
        username: str,
    ) -> Tuple[Optional[Dict[str, str]], results.Result]:
        with self.conn:
            with self.conn.cursor() as cursor:
                prepared_statement = self.find_prepared_statement(
                    "get_user_profile_by_username"
                )
                cursor.execute(
                    prepared_statement.execution_statement(),
                    (username,),
                )
                row = cursor.fetchone()
                if row is None:
                    return None, results.Result(
                        success=False, error_code=results.NONEXISTENT_USER_ERR
                    )
                user_id, email = row
                profile = {
                    "id": user_id,
                    "username": username,
                    "email": email,
                }
        return profile, results.Result(success=True)


def initialize_view(conn: Any) -> IdentityView:
    return IdentityView(conn=conn)
