import typing

from infrastructure.database.prepared_statements import PreparedStatement
from infrastructure.database.prepared_statements import sql


class PreparedStatementsMixin:
    def __init__(self):
        self.prepared_statements = sql.export()

    def find_prepared_statement(
        self,
        name: str,
    ) -> typing.Optional[PreparedStatement]:
        for ps in self.prepared_statements:
            if ps.name == name:
                return ps
        return None
