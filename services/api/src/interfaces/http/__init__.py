from flask import Flask


def create_app():
    app = Flask(__name__)

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
