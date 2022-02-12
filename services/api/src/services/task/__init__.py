import typing

from services import Service
from application import results


class TaskService(Service):
    def __init__(
        self,
        conn: typing.Any,
        subject_limit: int,
        description_limit: int,
    ):
        self.conn = conn
        self.subject_limit = subject_limit
        self.description_limit = description_limit
        super().__init__()

    def create_task(
        self, subject: str, description: str
    ) -> typing.Tuple[str, results.Result]:
        if len(subject) > self.subject_limit:
            return "", results.Result(
                success=False, error_code=results.TASK_SUBJECT_TOO_LONG
            )
        if len(description) > self.description_limit:
            return "", results.Result(
                success=False, error_code=results.TASK_DESCRIPTION_TOO_LONG
            )
        task_id = self.generate_unique_id()
        with self.conn:
            with self.conn.cursor() as cursor:
                prepared_statement = self.find_prepared_statement("add_task")
                cursor.execute(
                    prepared_statement.execution_statement(),
                    (task_id, subject, description),
                )
        return task_id, results.Result(success=True)

    def delete_task(self, task_id: str) -> results.Result:
        with self.conn:
            with self.conn.cursor() as cursor:
                prepared_statement = self.find_prepared_statement("remove_task")
                cursor.execute(
                    prepared_statement.execution_statement(),
                    (task_id,),
                )
                row = cursor.fetchone()
                if row[0] == 0:
                    return results.Result(
                        success=False, error_code=results.NONEXISTENT_TASK_ERR
                    )
        return results.Result(success=True)

    def update_task(
        self, task_id: str, subject: str, description: str, completed: bool
    ) -> results.Result:
        with self.conn:
            with self.conn.cursor() as cursor:
                prepared_statement = self.find_prepared_statement("update_task")
                cursor.execute(
                    prepared_statement.execution_statement(),
                    (subject, description, completed, task_id),
                )
                row = cursor.fetchone()
                if row[0] == 0:
                    return results.Result(
                        success=False, error_code=results.NONEXISTENT_TASK_ERR
                    )
        return results.Result(success=True)

    def create_user_task(
        self, username: str, subject: str, description: str
    ) -> typing.Tuple[str, results.Result]:
        if len(subject) > self.subject_limit:
            return "", results.Result(
                success=False, error_code=results.TASK_SUBJECT_TOO_LONG
            )
        if len(description) > self.description_limit:
            return "", results.Result(
                success=False, error_code=results.TASK_DESCRIPTION_TOO_LONG
            )
        task_id = self.generate_unique_id()
        with self.conn:
            with self.conn.cursor() as cursor:
                prepared_statement = self.find_prepared_statement(
                    "add_user_task"
                )
                cursor.execute(
                    prepared_statement.execution_statement(),
                    (username, task_id, subject, description),
                )
        return task_id, results.Result(success=True)

    def delete_user_task(self, username: str, task_id: str) -> results.Result:
        with self.conn:
            with self.conn.cursor() as cursor:
                prepared_statement = self.find_prepared_statement(
                    "remove_user_task"
                )
                cursor.execute(
                    prepared_statement.execution_statement(),
                    (username, task_id),
                )
        return results.Result(success=True)


def initialize_service(
    conn: typing.Any,
    subject_limit: int = 100,
    description_limit: int = 1000,
) -> TaskService:
    return TaskService(
        conn=conn,
        subject_limit=subject_limit,
        description_limit=description_limit,
    )
