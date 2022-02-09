import typing

from infrastructure.database.prepared_statements import PreparedStatement


class PreparedStatementsMixin:
    def find_prepared_statement(
        self,
        name: str,
    ) -> typing.Optional[PreparedStatement]:
        for ps in self.prepared_statements:
            if ps.name == name:
                return ps
        return None
