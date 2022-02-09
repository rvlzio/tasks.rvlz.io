import typing
from dataclasses import dataclass


@dataclass
class PreparedStatement:
    name: str
    statement: str
    args: int

    def prepared_statement(self) -> str:
        return f"PREPARE {self.name} AS {self.statement}"

    def execution_statement(self) -> str:
        params = ", ".join(["%s"] * self.args)
        return f"EXECUTE {self.name} ({params})"


def run_prepared_statements(
    conn: typing.Any,
    prepared_statements: typing.List[PreparedStatement],
):
    for ps in prepared_statements:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(ps.prepared_statement())
