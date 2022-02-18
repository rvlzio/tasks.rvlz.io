from flask import Blueprint, g, request

from interfaces.http.config import Config
from interfaces.http.middleware import authentication
from services.session import initialize_service


def create_controller(config: Config) -> Blueprint:
    app = Blueprint("sessions", __name__)

    @app.route("", methods=["POST"])
    @authentication.basic_authentication
    @authentication.required
    def _log_in():
        subject = g.subject
        service = initialize_service(
            conn=g.token_store_conn,
            secret_key=config.SECRET_KEY,
        )
        token, result = service.start_session(subject)
        if not result.success:
            return {
                "code": "internal_server_error",
                "message": "Internal server error.",
            }, 500
        return {"token": token}, 201

    @app.route("", methods=["DELETE"])
    @authentication.token_authentication
    @authentication.required
    def _log_out():
        header = request.headers["Authorization"]
        token = header.replace("Bearer ", "")
        service = initialize_service(
            conn=g.token_store_conn,
            secret_key=config.SECRET_KEY,
        )
        result = service.end_session(token)
        if not result.success:
            return {
                "code": "internal_server_error",
                "message": "Internal server error.",
            }, 500
        return "", 204

    return app
