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

NONEXISTENT_USER_ERR = ErrorCode(
    description="nonexisting_user",
)

INVALID_HMAC_TAG_ERR = ErrorCode(
    description="invalid_hmac_tag",
)

BAD_BASE64_ENCODING_ERR = ErrorCode(
    description="bad_base64_encoding",
)

MALFORMED_SESSION_TOKEN_ERR = ErrorCode(
    description="malformed_session_token",
)

MISSING_SESSION_ERR = ErrorCode(
    description="missing_session",
)

TASK_SUBJECT_TOO_LONG = ErrorCode(
    description="task_subject_too_long",
)
