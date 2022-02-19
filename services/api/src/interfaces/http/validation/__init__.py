import binascii
import base64
import json
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass

from interfaces.http.validation import errors as err
from interfaces.http.config import Config


@dataclass
class FieldError:
    name: str
    error_code: err.ErrorCode
    data: Optional[Dict] = None


@dataclass
class Result:
    success: bool
    error_code: Optional[err.ErrorCode] = None
    data: Optional[Dict] = None
    field_errors: Optional[List[FieldError]] = None


class Validator:
    def __init__(self, config: Config):
        self._config = config

    def parse_basic_auth_credentials(
        self, header: Optional[str]
    ) -> Tuple[str, str, Result]:
        if header is None:
            return (
                "",
                "",
                Result(
                    success=False,
                    error_code=err.MISSING_AUTHORIZATION_HEADER,
                ),
            )
        if not header.startswith("Basic "):
            return (
                "",
                "",
                Result(
                    success=False,
                    error_code=err.BAD_BASIC_AUTH_AUTHORIZATION_HEADER,
                ),
            )
        raw_credentials = header.replace("Basic ", "")
        try:
            credentials = base64.b64decode(raw_credentials).decode("utf-8")
        except (binascii.Error, UnicodeError):
            return (
                "",
                "",
                Result(
                    success=False,
                    error_code=err.BAD_BASIC_AUTH_AUTHORIZATION_HEADER,
                ),
            )
        if credentials.count(":") != 1:
            return (
                "",
                "",
                Result(
                    success=False,
                    error_code=err.BAD_BASIC_AUTH_AUTHORIZATION_HEADER,
                ),
            )
        field_errors = []
        username, password = credentials.split(":")
        if len(username) > self._config.MAXIMUM_USERNAME_LENGTH:
            field_errors.append(
                FieldError(
                    name="username",
                    error_code=err.MAXIMUM_LENGTH_NOT_MET,
                    data={
                        "max_length": self._config.MAXIMUM_USERNAME_LENGTH,
                    },
                )
            )
        if len(username) < self._config.MINIMUM_USERNAME_LENGTH:
            field_errors.append(
                FieldError(
                    name="username",
                    error_code=err.MINIMUM_LENGTH_NOT_MET,
                    data={
                        "min_length": self._config.MINIMUM_USERNAME_LENGTH,
                    },
                )
            )
        if len(password) > self._config.MAXIMUM_PASSWORD_LENGTH:
            field_errors.append(
                FieldError(
                    name="password",
                    error_code=err.MAXIMUM_LENGTH_NOT_MET,
                    data={
                        "max_length": self._config.MAXIMUM_PASSWORD_LENGTH,
                    },
                )
            )
        if len(password) < self._config.MINIMUM_PASSWORD_LENGTH:
            field_errors.append(
                FieldError(
                    name="password",
                    error_code=err.MINIMUM_LENGTH_NOT_MET,
                    data={
                        "min_length": self._config.MINIMUM_PASSWORD_LENGTH,
                    },
                )
            )
        if not username.isascii():
            field_errors.append(
                FieldError(
                    name="username",
                    error_code=err.NONASCII_CHARACTERS_PROVIDED,
                )
            )
        if not password.isascii():
            field_errors.append(
                FieldError(
                    name="password",
                    error_code=err.NONASCII_CHARACTERS_PROVIDED,
                )
            )
        if field_errors != []:
            return (
                "",
                "",
                Result(
                    success=False,
                    error_code=err.INVALID_FIELDS,
                    field_errors=field_errors,
                ),
            )
        return username, password, Result(success=True)

    def parse_bearer_auth_credentials(
        self, header: Optional[str]
    ) -> Tuple[str, Result]:
        if header is None:
            return "", Result(
                success=False,
                error_code=err.MISSING_AUTHORIZATION_HEADER,
            )
        if not header.startswith("Bearer "):
            return "", Result(
                success=False,
                error_code=err.BAD_BEARER_AUTH_AUTHORIZATION_HEADER,
            )
        token = header.replace("Bearer ", "")
        return token, Result(success=True)

    def parse_task_input_body(
        self, body: Optional[bytes]
    ) -> Tuple[str, str, Result]:
        if body is None or body == b"":
            return (
                "",
                "",
                Result(
                    success=False,
                    error_code=err.EMPTY_BODY,
                ),
            )
        try:
            payload = json.loads(body)
        except:
            return (
                "",
                "",
                Result(
                    success=False,
                    error_code=err.INVALID_JSON,
                ),
            )
        field_errors = []
        if "subject" not in payload:
            field_errors.append(
                FieldError(
                    name="subject",
                    error_code=err.MISSING_FIELD,
                )
            )
        else:
            if type(payload["subject"]) != str:
                field_errors.append(
                    FieldError(
                        name="subject",
                        error_code=err.INVALID_DATA_TYPE,
                        data={"type": "string"},
                    )
                )
        if "description" not in payload:
            field_errors.append(
                FieldError(
                    name="description",
                    error_code=err.MISSING_FIELD,
                )
            )
        else:
            if type(payload["description"]) != str:
                field_errors.append(
                    FieldError(
                        name="description",
                        error_code=err.INVALID_DATA_TYPE,
                        data={"type": "string"},
                    )
                )
        if field_errors != []:
            return (
                "",
                "",
                Result(
                    success=False,
                    error_code=err.INVALID_FIELDS,
                    field_errors=field_errors,
                ),
            )
        return payload["subject"], payload["description"], Result(success=True)

    def find_error_response(self, result: Result) -> Tuple[Dict, int]:
        error_code = result.error_code
        if error_code == err.MISSING_AUTHORIZATION_HEADER:
            return {
                "code": error_code.description,
                "message": "'Authorization' header required.",
            }, 401
        if error_code == err.BAD_BASIC_AUTH_AUTHORIZATION_HEADER:
            return {
                "code": error_code.description,
                "message": (
                    "Bad 'Authorization' header for basic authentication."
                ),
            }, 401
        if error_code == err.BAD_BEARER_AUTH_AUTHORIZATION_HEADER:
            return {
                "code": error_code.description,
                "message": (
                    "Bad 'Authorization' header for token authentication."
                ),
            }, 401
        if error_code == err.EMPTY_BODY:
            return {
                "code": error_code.description,
                "message": "Empty body not allowed.",
            }, 400
        if error_code == err.INVALID_JSON:
            return {
                "code": error_code.description,
                "message": "Invalid JSON in body.",
            }, 422
        if error_code == err.INVALID_FIELDS:
            fields = {}
            for field_error in result.field_errors:
                if field_error.name not in fields:
                    fields[field_error.name] = []
                field_payload = {
                    "code": field_error.error_code.description,
                }
                if field_error.error_code == err.MAXIMUM_LENGTH_NOT_MET:
                    limit = field_error.data.get("max_length")
                    field_payload["reason"] = (
                        f"'{field_error.name}' cannot be longer "
                        f"than {limit} characters."
                    )
                elif field_error.error_code == err.MINIMUM_LENGTH_NOT_MET:
                    limit = field_error.data.get("min_length")
                    field_payload["reason"] = (
                        f"'{field_error.name}' cannot be shorter "
                        f"than {limit} characters."
                    )
                elif (
                    field_error.error_code == err.NONASCII_CHARACTERS_PROVIDED
                ):
                    field_payload["reason"] = (
                        f"'{field_error.name}' must only "
                        "have ASCII characters."
                    )
                elif field_error.error_code == err.MISSING_FIELD:
                    field_payload["reason"] = "Missing."
                elif field_error.error_code == INVALID_DATA_TYPE:
                    data_type = field_error.data["type"]
                    field_payload[
                        "reason"
                    ] = f"Only type {data_type}' allowed."
                fields[field_error.name].append(field_payload)
            payload = {
                "code": error_code.description,
                "message": "Invalid field(s).",
                "fields": fields,
            }
            return payload, 401
        return {
            "code": "internal_server_error",
            "message": "Internal server error",
        }, 500


def load_validator(config: Config) -> Validator:
    return Validator(config)
