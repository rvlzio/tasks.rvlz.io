from flask import Flask, g, request
from interfaces.http import controllers
from infrastructure import database, token_store
from interfaces.http import config


def create_app():
    app = Flask(__name__)
    cfg = config.load()
    database_connection = database.generate_connection(cfg)
    token_store_connection = token_store.generate_connection(cfg)
    database.run_all_prepared_statements(database_connection)

    @app.before_request
    def _check_content_type():
        methods = ["POST", "PUT", "PATCH"]
        content_type = request.headers.get("content-type", "")
        if (
            request.method in methods
            and content_type.lower() != "application/json"
        ):
            payload = {
                "code": "unsupported_media_type",
                "message": "Only application/json accepted as content type",
            }
            return payload, 415

    @app.before_request
    def _set_database_connection():
        g.database_conn = database_connection
        g.token_store_conn = token_store_connection

    app.register_blueprint(controllers.sessions(), url_prefix="/v1/sessions")
    app.register_blueprint(controllers.tasks(), url_prefix="/v1/tasks")

    @app.route("/v1/health_check")
    def _health_check():
        return "healthy", 200

    @app.after_request
    def _general_headers(response):
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "0"
        response.headers["Cache-Control"] = "no-store"
        response.headers[
            "Content-Security-Policy"
        ] = "default-src 'none'; frame-ancestors 'none'; sandbox"
        return response

    return app
