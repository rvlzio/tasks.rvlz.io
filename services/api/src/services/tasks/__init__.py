import typing

from services import Service
from application import results


class TaskService(Service):
    def __init__(self, conn: typing.Any):
        self.conn = conn
        super().__init__()

    def create(
        self, subject: str, description: str
    ) -> typing.Tuple[str, results.Result]:
        task_id = self.generate_unique_id()
        with self.conn:
            with self.conn.cursor() as cursor:
                prepared_statement = self.find_prepared_statement("add_task")
                cursor.execute(
                    prepared_statement.execution_statement(),
                    (task_id, subject, description),
                )
        return task_id, results.Result(success=True)


def initialize_service(conn: typing.Any) -> TaskService:
    return TaskService(conn=conn)
