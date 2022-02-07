import typing
from dataclasses import dataclass


@dataclass
class ErrorCode:
    description: str


@dataclass
class Result:
    success: bool
    error_code: typing.Optional[ErrorCode] = None
