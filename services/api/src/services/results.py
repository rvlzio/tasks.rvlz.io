import typing
from dataclasses import dataclass


@dataclass
class ErrorCode:
    description: str


@dataclass
class Result:
    success: bool
    error_code: typing.Optional[ErrorCode] = None


DUPLICATE_USERNAME_ERR = ErrorCode(
    description="duplicate_username",
)

DUPLICATE_EMAIL_ERR = ErrorCode(
    description="duplicate_email",
)

INVALID_CREDENTIALS_ERR = ErrorCode(
    description="invalid_credentials",
)
