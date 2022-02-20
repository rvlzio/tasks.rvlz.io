from typing import Any, Tuple, Dict

from flask import Blueprint, g, request, make_response

from interfaces.http.config import Config
from interfaces.http.validation import Validator, Result
from interfaces.http.middleware import authentication
from services import task as task_service
from views import task as task_view


class Controller:
    def __init__(self, config: Config, validator: Validator):
        self.config = config
        self.validator = validator

    def extract(self, request: Any) -> Tuple[str, str, Result]:
        body = request.get_data()
        return self.validator.parse_task_input_body(body)

    def find_error_response(self, result: Result) -> Tuple[Dict, int]:
        return self.validator.find_error_response(result)

    def __call__(self) -> Blueprint:
        controller = Blueprint("tasks", __name__)

        @controller.route("", methods=["POST"])
        @authentication.token_authentication
        @authentication.required
        def _create_task():
            username = g.subject
            subject, description, result = self.extract(request)
            if not result.success:
                payload, status_code = self.find_error_response(result)
                return payload, status_code
            service = task_service.initialize_service(g.database_conn)
            task_id, result = service.create_user_task(
                username=username,
                subject=subject,
                description=description,
            )
            if not result.success:
                return {
                    "code": "internal_server_error",
                    "message": "Internal server error.",
                }, 500
            response = make_response("", 201)
            response.headers["Location"] = f"/v1/tasks/{task_id}"
            response.autocorrect_location_header = False
            return response

        @controller.route("/<string:task_id>", methods=["GET"])
        @authentication.token_authentication
        @authentication.required
        def _read_task(task_id):
            username = g.subject
            view = task_view.initialize_view(g.database_conn)
            task, result = view.current_user_task(username, task_id)
            task["id"] = task_id
            if not result.success:
                return {
                    "code": "task_not_found",
                    "message": "Task could not be found.",
                }, 404
            return task, 200

        return controller
