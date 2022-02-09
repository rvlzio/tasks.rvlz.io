import typing

from infrastructure.database.prepared_statements import PreparedStatement
from infrastructure.database.prepared_statements import mixin


class View(mixin.PreparedStatementsMixin):
    pass
