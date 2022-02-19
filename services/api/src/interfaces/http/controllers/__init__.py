from interfaces.http.controllers import sessions as _sessions
from interfaces.http.controllers import tasks as _tasks
from interfaces.http import config
from interfaces.http.validation import Validator

_config = config.load()
_validator = Validator(config)
sessions = _sessions.Controller(_config)
tasks = _tasks.Controller(_config, _validator)
