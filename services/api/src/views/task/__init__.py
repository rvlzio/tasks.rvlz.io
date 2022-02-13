from typing import Tuple, Optional, Dict, Any

from views import View
from application import results


class TaskView(View):
    def __init__(self, conn: Any):
        self.conn = conn
        super().__init__()

    def current_task(
        self, task_id: str
    ) -> Tuple[Optional[Dict[str, Any]], results.Result]:
        with self.conn:
            with self.conn.cursor() as cursor:
                prepared_statement = self.find_prepared_statement("find_task")
                cursor.execute(
                    prepared_statement.execution_statement(),
                    (task_id,),
                )
                row = cursor.fetchone()
                if row is None:
                    return None, results.Result(
                        success=False,
                        error_code=results.NONEXISTENT_TASK_ERR,
                    )
                subject, description, completed = row
                data = {
                    "subject": subject,
                    "description": description,
                    "completed": completed,
                }
        return data, results.Result(success=True)

    def current_user_task(
        self, username: str, task_id: str
    ) -> Tuple[Optional[Dict[str, Any]], results.Result]:
        with self.conn:
            with self.conn.cursor() as cursor:
                prepared_statement = self.find_prepared_statement(
                    "find_user_task"
                )
                cursor.execute(
                    prepared_statement.execution_statement(),
                    (username, task_id),
                )
                row = cursor.fetchone()
                if row is None:
                    return None, results.Result(
                        success=False, error_code=results.NONEXISTENT_TASK_ERR
                    )
                subject, description, completed = row
                data = {
                    "subject": subject,
                    "description": description,
                    "completed": completed,
                }
        return data, results.Result(success=True)


def initialize_view(conn: Any) -> TaskView:
    return TaskView(conn=conn)
