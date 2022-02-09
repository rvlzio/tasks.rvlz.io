import typing
import os
import base64

from infrastructure.database.prepared_statements import PreparedStatement
from infrastructure.database.prepared_statements import mixin


class Service(mixin.PreparedStatementsMixin):
    def generate_unique_id(self) -> str:
        return base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
