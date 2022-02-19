from flask import Blueprint, g, request

from interfaces.http.config import Config
from interfaces.http.middleware import authentication
from services.session import initialize_service


class Controller:
    def __init__(self, config: Config):
        self.config = config

    def __call__(self) -> Blueprint:
        controller = Blueprint("session", __name__)

        @controller.route("", methods=["POST"])
        @authentication.basic_authentication
        @authentication.required
        def _log_in():
            username = g.subject
            service = initialize_service(
                conn=g.token_store_conn,
                secret_key=self.config.SECRET_KEY,
            )
            token, result = service.start_session(username)
            if not result.success:
                return {
                    "code": "internal_server_error",
                    "message": "Internal server error.",
                }, 500
            return {"token": token}, 201

        @controller.route("", methods=["DELETE"])
        @authentication.token_authentication
        @authentication.required
        def _delete_task():
            header = request.headers["Authorization"]
            token = header.replace("Bearer ", "")
            service = initialize_service(
                conn=g.token_store_conn,
                secret_key=self.config.SECRET_KEY,
            )
            result = service.end_session(token)
            if not result.success:
                return {
                    "code": "internal_server_error",
                    "message": "Internal server error.",
                }, 500
            return "", 204

        return controller
