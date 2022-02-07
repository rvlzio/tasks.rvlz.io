import typing
import os
import base64

from infrastructure.database import PreparedStatement


class Service:
    def find_prepared_statement(
        self,
        name: str,
    ) -> typing.Optional[PreparedStatement]:
        for ps in self.prepared_statements:
            if ps.name == name:
                return ps
        return None

    def generate_unique_id(self) -> str:
        return base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
