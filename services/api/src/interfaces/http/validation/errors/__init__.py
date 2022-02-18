from dataclasses import dataclass


@dataclass
class ErrorCode:
    description: str


# Top-level error codes

MISSING_AUTHORIZATION_HEADER = ErrorCode(
    description="missing_authorization_header"
)

BAD_BASIC_AUTH_AUTHORIZATION_HEADER = ErrorCode(
    description="bad_basic_auth_authorization_header"
)

BAD_BEARER_AUTH_AUTHORIZATION_HEADER = ErrorCode(
    description="bad_bearer_auth_authorization_header"
)

INVALID_FIELDS = ErrorCode(description="invalid_fields")

# Field-level error codes

MAXIMUM_LENGTH_NOT_MET = ErrorCode(description="maximum_length_not_met")

MINIMUM_LENGTH_NOT_MET = ErrorCode(description="minimum_length_not_met")

NONASCII_CHARACTERS_PROVIDED = ErrorCode(
    description="nonascii_characters_provided"
)
